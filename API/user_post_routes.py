from http.client import (
    CONFLICT,
    INTERNAL_SERVER_ERROR,
    NOT_FOUND,
    UNPROCESSABLE_ENTITY,
)
from uuid import UUID, uuid4

import Database.db_mapping as tables
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from Database import schemas
from Database.utils import (
    AsyncSession,
    gerar_refresh_token,
    gerar_session_token,
    redis_pool,
    set_refresh_token_cookie,
    set_session_token_cookie,
)
from email_verify import enviar_email_verificacao
from fastapi import BackgroundTasks, Body, FastAPI, HTTPException, Request, Response
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr, validate_email
from pydantic_core import PydanticCustomError
from sqlalchemy import exc, insert, or_, select

hasher = PasswordHasher()

USER_API = FastAPI(title="Rotas POST para serivços de usuários")


async def search_for_user(username: str, email: EmailStr):
    async with AsyncSession() as session:
        try:
            transaction = session.begin()
            await session.scalars(
                insert(tables.Usuario).values(
                    username=username, email=email, password="abc"
                )
            )
        except exc.IntegrityError as e:
            if "uq_usuario_username" in str(e):
                raise HTTPException(
                    CONFLICT, "Esse nome de usuário já está sendo usado!"
                )
            if "uq_usuario_email" in str(e):
                raise HTTPException(CONFLICT, "Esse email já está sendo usado!")
        else:
            transaction.rollback()
            return True


@USER_API.post("/register")
async def begin_register(user: schemas.UserRegistro, bg_tasks: BackgroundTasks):
    """Envia um email de confirmação do cadastro para o email fornecido,
    depois armazena os dados fornecidos no redis para validar o cadastro"""

    try:
        validate_email(user.email)
    except PydanticCustomError:
        raise HTTPException(UNPROCESSABLE_ENTITY, "Email Inválido")

    search_for_user()

    protocolo_usuario = uuid4()
    bg_tasks.add_task(
        enviar_email_verificacao,
        user.email,
        protocol=protocolo_usuario,
        username=user.username,
    )

    with redis_pool() as cache_storage:
        cache_storage.hset(f"protocol:{protocolo_usuario}", mapping=user.model_dump())
        cache_storage.expire(
            f"protocol:{protocolo_usuario}", 1800
        )  # 1800 segundos == 30 min


@USER_API.get("/register/confirm/{protocol}")
async def create_register(
    protocol: UUID, http_response: Response, http_request: Request
):
    """Efetiva o registro no banco
    recebendo uma requisição referente ao protocolo gerado"""

    with redis_pool() as cache_storage:
        user_data = cache_storage.hgetall(f"protocol:{protocol}")

        if not user_data:
            raise HTTPException(
                NOT_FOUND, "Protocolo inválido, já finalizado, ou expirado"
            )

        user_data["password"] = hasher.hash(user_data.get("password"))

    async with AsyncSession() as session:
        try:
            await session.execute(insert(tables.Usuario).values(user_data))

        except exc.IntegrityError as e:
            if "uq_usuario_username" in str(e):
                raise HTTPException(
                    CONFLICT, "Esse nome de usuário já está sendo usado!"
                )
            if "uq_usuario_email" in str(e):
                raise HTTPException(CONFLICT, "Esse email já está sendo usado!")
        else:
            try:
                set_session_token_cookie(
                    http_response, await gerar_session_token(user_data.get("email"))
                )
            except jwt.exceptions.PyJWTError:
                raise HTTPException(
                    INTERNAL_SERVER_ERROR, "Erro desconhecido gerando token"
                )
            else:
                await session.flush()
                await session.commit()
                redis_pool().delete(f"protocol:{protocol}")
                return Jinja2Templates("./Html_Templates").TemplateResponse(
                    http_request, "confirm_register.html"
                )


@USER_API.post("/login")
async def login_user(user: schemas.UserLogin, http_response: Response):
    """Procura o usuário no banco e valida a senha,
    se válida retorna 2 tokens, senão, levanta erro"""

    async with AsyncSession() as session:
        result = await session.execute(
            select(tables.Usuario).where(
                or_(
                    tables.Usuario.username == user.login_key,
                    tables.Usuario.email == user.login_key,
                )
            )
        )

        found = result.scalars().first()

    if found is None:
        raise HTTPException(NOT_FOUND, "Usuário não encontrado")

    try:
        hasher.verify(found.password, user.password)
    except VerifyMismatchError:
        raise HTTPException(NOT_FOUND, "Senha incorreta")

    try:
        session_token = await gerar_session_token(found.id_usuario)
        await set_session_token_cookie(http_response, session_token)

        if user.keep_login:
            refresh_token = await gerar_refresh_token(found.id_usuario)
            await set_refresh_token_cookie(http_response, refresh_token)

    except jwt.exceptions.PyJWTError as e:
        raise HTTPException(
            INTERNAL_SERVER_ERROR, f"Erro desconhecido gerando token, {e}"
        )

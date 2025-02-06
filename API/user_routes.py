from asyncio import create_task
from uuid import UUID, uuid4

import Database.db_mapping as tables
import jwt
import schemas
from argon2 import PasswordHasher
from Database.utils import (
    AsyncSession,
    generate_refresh_token,
    generate_session_token,
    generate_register_token,
    redis_pool
)
from Email.email_verify import send_verification_mail
from fastapi import FastAPI, HTTPException
from pydantic import validate_email
from pydantic_core import PydanticCustomError
from sqlalchemy import exc, insert, or_, select

hasher = PasswordHasher()
POST_APP = FastAPI(title="Main API POST Routes")


@POST_APP.post("/register")
async def begin_register(user: schemas.UserRegister):
    """Envia um email de confirmação do cadastro para o email fornecido,
    depois armazena os dados fornecidos em um cache para validar o cadastro"""

    try:
        validate_email(user.email)
    except PydanticCustomError:
        raise HTTPException(422, "Email Inválido")

    # Envia o email assíncronamente
    request_protocol = uuid4()
    await create_task(
        send_verification_mail(
            user.email, protocol=request_protocol, username=user.username
        )
    )

    # Armazena os dados do usuário em cache
    with redis_pool() as cache_storage:
        cache_storage.hset(f"protocol:{request_protocol}", mapping=user.model_dump())
        cache_storage.expire(
            f"protocol:{request_protocol}", 1800
        )  # 1800 segundos == 30 min


@POST_APP.get("/register/confirm/{protocol}")
async def create_register(protocol: UUID):
    """Efetiva o registro no banco
    recebendo uma requisição referente ao protocolo gerado"""

    # Obtem os dados do usuário no cache
    with redis_pool() as cache_storage:
        user_data = cache_storage.hgetall(f"protocol:{protocol}")

        if not user_data:
            raise HTTPException(404, "Protocolo inválido ou expirado")

        user_data["password"] = hasher.hash(user_data.get("password"))

    # Tenta criar o usuário no banco
    async with AsyncSession() as session:
        try:
            await session.execute(insert(tables.Usuario).values(user_data))

        # Tratamento para duplicidade
        except exc.IntegrityError as e:
            if "uq_usuario_username" in str(e):
                raise HTTPException(409, "Esse nome de usuário já está sendo usado!")
            if "uq_usuario_email" in str(e):
                raise HTTPException(409, "Esse email já está sendo usado!")
        else:
            try:
                token = await generate_register_token(email=user_data.get("email"))
            except jwt.exceptions.PyJWTError:
                raise HTTPException(500, "Erro desconhecido gerando token")
            else:
                await session.flush()
                await session.commit()
                redis_pool().delete(f"protocol:{protocol}")
                return {"token": token}


@POST_APP.post("/login")
async def login_user(user: schemas.UserLogin):
    """Procura o usuário no banco e valida a senha,
    se válida retorna 2 tokens, senão, levanta erro"""

    async with AsyncSession() as a_ssession:
        # Busca o usuário no banco
        result = await a_ssession.execute(
            select(tables.Usuario).where(
                or_(
                    tables.Usuario.username == user.login_key,
                    tables.Usuario.email == user.login_key,
                )
            )
        )

    found = result.scalars().first()

    # Verifica se existe
    if not found:
        raise HTTPException(404, "Usuário não encontrado")

    # Verifica a senha se o usuário existir
    if not hasher.verify(found.password, user.password):
        raise HTTPException(401, "Senha incorreta")

    # Se não houverem erros retorna os tokens
    try:
        if not user.keep_login:
            token = generate_session_token(found.id_usuario, expire_in_a_day=True)

            return {"session_token": token}

        ref_token = generate_refresh_token(found.id_usuario)
        ses_token = generate_session_token(found.id_usuario)

        return {
            "refresh_token": ref_token,
            "session_token": ses_token,
        }

    except jwt.exceptions.PyJWTError:
        raise HTTPException(500, "Erro desconhecido gerando token")

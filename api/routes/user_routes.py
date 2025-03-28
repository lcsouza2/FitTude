from uuid import UUID, uuid4

from ..database import db_mapping as tables
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from core.email_verify import send_verification_mail
from fastapi import APIRouter, BackgroundTasks, Depends, Request, Response
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr, validate_email
from pydantic_core import PydanticCustomError
from sqlalchemy import exc, insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from core import schemas
from core.authetication import TokenService
from core.config import Config
from core.exceptions import (
    InvalidCredentials,
    InvalidRegisterProtocol,
    UniqueConstraintViolation,
)
from core.utils import cached_operation, db_operation, redis_pool

USER_ROUTER = APIRouter(prefix="/api/user")

hasher = PasswordHasher()


@cached_operation(timeout=3600)
@db_operation
async def search_for_user(
    username: str, email: EmailStr, session
) -> bool:
    """
    Check if username or email are already registered.
    Returns True if user can be created (no conflicts found).
    Raises UniqueConstraintViolation if conflicts exist.
    """
    result = await session.execute(
        select(tables.Usuario).where(
            or_(tables.Usuario.username == username, tables.Usuario.email == email)
        )
    )

    if user := result.scalar_one_or_none():
        if user.username == username:
            raise UniqueConstraintViolation("Username já está em uso")
        raise UniqueConstraintViolation("Email já está em uso")

    return True


@USER_ROUTER.post("/register")
async def begin_register(user: schemas.UserRegistro, bg_tasks: BackgroundTasks):
    """Envia um email de confirmação do cadastro para o email fornecido,
    depois armazena os dados fornecidos no redis para validar o cadastro"""

    try:
        validate_email(user.email)
    except PydanticCustomError:
        raise InvalidCredentials("Email inválido")

    await search_for_user(user.username, user.email)

    user_protocol = uuid4()
    bg_tasks.add_task(
        send_verification_mail,
        user.email,
        protocol=user_protocol,
        username=user.username,
    )

    async with redis_pool() as cache_storage:
        await cache_storage.hset(f"protocol:{user_protocol}", mapping=user.model_dump())
        await cache_storage.expire(
            f"protocol:{user_protocol}", 1800
        )  # 1800 segundos == 30 min


@db_operation
@USER_ROUTER.get("/register/confirm/{protocol}")
async def create_register(
    session,
    protocol: UUID,
    token_service: TokenService = Depends(TokenService)
):
    """Efetiva o registro no banco
    recebendo uma requisição referente ao protocolo gerado"""

    async with redis_pool() as redis:
        user_data = await redis.hgetall(f"protocol:{protocol}")

        if not user_data:
            raise InvalidRegisterProtocol()

        user_data["password"] = hasher.hash(user_data.get("password"))

        try:
            created_user = await session.execute(
                insert(tables.Usuario)
                .values(user_data)
                .returning(tables.Usuario.id_usuario)
            )

        except exc.IntegrityError as e:
            if "uq_usuario_username" in str(e):
                raise UniqueConstraintViolation("Esse username já está sendo usado!")

            raise UniqueConstraintViolation("Esse email já está sendo usado!")
        else:
            session_token = await token_service.generate_session_token(created_user)
            refresh_token = await token_service.generate_refresh_token(created_user)

            token_service.set_refresh_token_cookie(token_service.response, refresh_token)

            await session.commit()

            redis.delete(f"protocol:{protocol}")

            return Jinja2Templates("./Html_Templates").TemplateResponse(
                "confirm_register.html",
                {
                    "request": token_service.request,
                    "acess_token": session_token,
                    "token_type": "Bearer",
                    "expires_in": int(Config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
                },
            )


@db_operation
@USER_ROUTER.post("/login")
async def login_user(
    user: schemas.UserLogin,
    session,
    token_service: TokenService = Depends(TokenService),
):
    """Procura o usuário no banco e valida a senha,
    se válida retorna 2 tokens, senão, levanta erro"""

    result = await session.execute(
        select(tables.Usuario).where(
            or_(
                tables.Usuario.username == user.login_key,
                tables.Usuario.email == user.login_key,
            )
        )
    )

    found = result.scalars().one_or_none()

    if found is None:
        raise InvalidCredentials("Usuário não encontrado")

    try:
        hasher.verify(found.password, user.password)
    except VerifyMismatchError:
        raise InvalidCredentials("Senha inválida")

    session_token = await token_service.generate_session_token(found.id_usuario)

    if not user.keep_login:
        token_service.refresh_expires = 86400  # 1 dia em segundos

    refresh_token = await token_service.generate_refresh_token(found.id_usuario)
    await token_service.set_refresh_token_cookie(token_service.response, refresh_token)

    return {
        "access_token": session_token,
        "token_type": "Bearer",
        "expires_in": int(token_service.session_expires.total_seconds()),
    }

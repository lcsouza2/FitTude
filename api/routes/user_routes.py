"""User authentication and registration routes.

This module handles all user-related operations including:
- User registration and email verification
- User login and session management
"""

import random
import string
from typing import Any
from uuid import UUID, uuid4

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, BackgroundTasks, Depends
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr, validate_email
from pydantic_core import PydanticCustomError
from sqlalchemy import exc, insert, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from core import schemas
from core.authetication import TokenService
from core.config import Config
from core.connections import db_connection, redis_connection
from core.email_service import send_pwd_change_mail, send_verification_mail
from core.exceptions import (
    InvalidCredentials,
    InvalidRegisterProtocol,
    UniqueConstraintViolation,
)
from core.utils import cached_operation

from ..database import db_mapping

USER_ROUTER = APIRouter(prefix="/api/user")

hasher = PasswordHasher()


def generate_user_protocol():
    return uuid4()


def generate_pwd_change_protocol():
    return "".join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(6)]
    )


async def save_register_protocol(user: schemas.User):
    protocol = generate_user_protocol()

    await send_verification_mail(user.email, protocol=protocol, username=user.username)

    async with redis_connection() as redis:
        await redis.hset(f"protocol:{protocol}", mapping=user.model_dump())
        await redis.expire(
            f"protocol:{protocol}",
            1800,  # 30 minutos
        )


async def save_pwd_change_protocol(user: schemas.UserPasswordChange):
    protocol = generate_pwd_change_protocol()

    await send_pwd_change_mail(user.email, protocol=protocol, username=user.username)

    async with redis_connection() as redis:
        await redis.hset(f"protocol:{protocol}", mapping=user.model_dump())
        await redis.expire(
            f"protocol:{protocol}",
            1800,  # 30 minutos
        )


async def _generate_auth_tokens(
    user_id: int,
    token_service: TokenService,
    long_session: bool = True,
) -> tuple[str, str]:
    """
    Generate authentication tokens for a user.

    Args:
        user_id (int): User ID to generate tokens for
        token_service (TokenService): Token service instance
        long_session (bool): If False, sets refresh token to 1 day

    Returns:
        tuple[str, str]: Session token and refresh token
    """
    if not long_session:
        token_service.refresh_expires = 86400  # 1 day in seconds

    session_token = await token_service.generate_session_token(user_id)
    refresh_token = await token_service.generate_refresh_token(user_id)

    return session_token, refresh_token


@cached_operation(timeout=3600)
async def search_for_user(
    username: str, email: EmailStr, session: AsyncSession = db_connection()
) -> str:
    """
    Check if a username or email is already registered in the database.

    Args:
        username (str): The username to check
        email (EmailStr): The email to check
        session (AsyncSession, optional): Database session. Defaults to db_connection()

    Returns:
        str: "Credenciais válidas" if no conflicts found

    Raises:
        UniqueConstraintViolation: If username or email already exists
    """
    result = await session.execute(
        select(db_mapping.Usuario).where(
            or_(
                db_mapping.Usuario.username == username,
                db_mapping.Usuario.email == email,
            )
        )
    )

    if user := result.scalar_one_or_none():
        if user.username == username:
            raise UniqueConstraintViolation("Username já está em uso")
        raise UniqueConstraintViolation("Email já está em uso")

    return "Credenciais válidas"


@USER_ROUTER.post("/register")
async def begin_register(
    user: schemas.UserRegistro, bg_tasks: BackgroundTasks
) -> dict[str, str]:
    """
    Start user registration process by sending verification email.

    This function:
    1. Validates the email format
    2. Checks if username/email are available
    3. Generates a unique protocol
    4. Sends verification email
    5. Stores registration data in Redis

    Args:
        user (schemas.UserRegistro): User registration data
        bg_tasks (BackgroundTasks): FastAPI background tasks handler

    Returns:
        dict[str, str]: Success message indicating email sent

    Raises:
        InvalidCredentials: If email format is invalid
        UniqueConstraintViolation: If username/email already exists
    """
    try:
        validate_email(user.email)
    except PydanticCustomError:
        raise InvalidCredentials("Email inválido")

    await search_for_user(user.username, user.email)

    bg_tasks.add_task(save_register_protocol, user=user)

    return {
        "message": """Email de verificação enviado.
        Por favor verifique sua caixa de entrada."""
    }


@USER_ROUTER.get("/register/confirm/{protocol}")
async def create_register(
    protocol: UUID,
    token_service: TokenService = Depends(TokenService),
    session: AsyncSession = Depends(db_connection),
):
    """
    Complete user registration by confirming email verification.

    This function:
    1. Retrieves registration data from Redis using protocol
    2. Hashes the user password
    3. Creates user record in database
    4. Generates session and refresh tokens
    5. Removes temporary Redis data

    Args:
        protocol (UUID): Registration verification protocol
        token_service (TokenService): Service for token operations
        session (AsyncSession): Database session

    Returns:
        TemplateResponse: Registration confirmation page with tokens

    Raises:
        InvalidRegisterProtocol: If protocol is invalid/expired
        UniqueConstraintViolation: If username/email became taken
    """

    async with redis_connection() as redis:
        user_data = await redis.hgetall(f"protocol:{protocol}")

        if not user_data:
            raise InvalidRegisterProtocol()

        user_data["password"] = hasher.hash(user_data.get("password"))

        try:
            created_user = await session.execute(
                insert(db_mapping.Usuario)
                .values(user_data)
                .returning(db_mapping.Usuario.id_usuario)
            )

        except exc.IntegrityError as e:
            if "uq_usuario_username" in str(e):
                raise UniqueConstraintViolation("Esse username já está sendo usado!")

            raise UniqueConstraintViolation("Esse email já está sendo usado!")

        else:
            session_token = refresh_token = _generate_auth_tokens(
                created_user, token_service, False
            )

            token_service.set_refresh_token_cookie(
                token_service.response, refresh_token
            )

            await session.commit()

            redis.delete(f"protocol:{protocol}")

            default_context = {
                "request": token_service.request,
                "acess_token": session_token,
                "token_type": "Bearer",
                "expires_in": int(Config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
            }

            return Jinja2Templates("./templates").TemplateResponse(
                "confirm_register.html", default_context
            )


@USER_ROUTER.post("/login")
async def login_user(
    user: schemas.UserLogin,
    session: AsyncSession = Depends(db_connection),
    token_service: TokenService = Depends(TokenService),
) -> dict[str, Any]:
    """
    Authenticate user and generate session tokens.
    """
    query = select(db_mapping.Usuario.id_usuario, db_mapping.Usuario.password).where(
        or_(
            db_mapping.Usuario.username == user.login_key,
            db_mapping.Usuario.email == user.login_key,
        )
    )

    async with session:
        result = await session.execute(query)
        if not (found := result.first()):
            raise InvalidCredentials("Usuário não encontrado")

        try:
            hasher.verify(found.password, user.password)
        except VerifyMismatchError:
            raise InvalidCredentials("Senha inválida")

        session_token, refresh_token = await _generate_auth_tokens(
            user_id=found.id_usuario,
            token_service=token_service,
            long_session=user.keep_login,
        )

        await token_service.set_refresh_token_cookie(
            token_service.response, refresh_token
        )

        return {
            "access_token": session_token,
            "token_type": "Bearer",
            "expires_in": int(token_service.session_expires.total_seconds()),
        }


@USER_ROUTER.post("/logout")
async def logout_user(
    token_service: TokenService = Depends(TokenService),
) -> dict[str, str]:
    """
    Logout user by deleting session and refresh tokens.
    """
    token_service.delete_refresh_token_cookie(token_service.response)

    return {"message": "Logout realizado com sucesso!"}


@USER_ROUTER.post("/password_change")
async def handle_password_change(background_tasks: BackgroundTasks, user: schemas.User):
    background_tasks.add_task(save_pwd_change_protocol, user=user)


@USER_ROUTER.post("/refresh_token")
async def send_refresh_token(
    token_service: TokenService = Depends(TokenService),
) -> dict[str, str]:
    """
    Refresh user session token.

    This function checks the validity of the refresh token and generates a new session token.
    """

    return {
        "access_token": await token_service.renew_token(token_service.request),
        "token_type": "Bearer",
        "expires_in": int(token_service.session_expires.total_seconds()),
    }

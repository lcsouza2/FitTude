"""User authentication and registration routes.

This module handles all user-related operations including:
- User registration and email verification
- User login and session management
"""

from typing import Any
from uuid import UUID, uuid4

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from email_validator import EmailNotValidError, validate_email
from fastapi import APIRouter, BackgroundTasks, Depends, Response
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr
from sqlalchemy import exc, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import schemas
from app.core.authentication import TokenService
from app.core.config import Config
from app.core.connections import db_connection, redis_connection
from app.core.email_service import EmailClient
from app.core.exceptions import (
    InvalidCredentials,
    InvalidProtocol,
    UniqueConstraintViolation,
)
from app.core.utils import generate_random_protocol
from app.database import db_mapping

USER_ROUTER = APIRouter(prefix="/api/user", tags=["User Related Routes"])
HASHER = PasswordHasher()


async def save_register_protocol(user: schemas.UserRegister):
    """
    Save user registration data in Redis and send verification email.
    This function:
    1. Generates a unique protocol
    2. Sends verification email
    3. Stores user data in Redis with 30 min expiration time
    Args:
        user (schemas.UserRegister): User registration data
    """

    protocol = uuid4()

    await EmailClient().send_register_verify_mail(
        dest_email=user.email, protocol=protocol, username=user.name.split(" ")[0]
    )

    async with redis_connection() as redis:
        await redis.hset(
            f"protocol:{protocol};type:register", mapping=user.model_dump()
        )
        await redis.expire(
            f"protocol:{protocol};type:register",
            1800,  # 30 min
        )


async def save_pwd_change_protocol(user: schemas.UserPwdChange):
    """
    Save user data in Redis and send verification email.
    This function:
    1. Generates a unique protocol
    2. Sends verification email
    3. Stores user data in Redis with 30 min expiration time
    Args:
        user (schemas.UserPwdChange): User registration data
    """
    protocol = generate_random_protocol()

    await EmailClient().send_pwd_change_mail(
        dest_email=user.email, char_protocol=protocol, username=user.name.split(" ")[0]
    )

    async with redis_connection() as redis:
        await redis.hset(
            f"protocol:{protocol};type:pwd_change", mapping=user.model_dump()
        )
        await redis.expire(
            f"protocol:{protocol};type:pwd_change",
            1800,  # 30 min
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


async def search_for_user(email: EmailStr) -> str:
    """
    Check if a username or email is already registered in the database.

    Args:
        email (EmailStr): The email to check

    Returns:
        bool: True if no conflicts found

    Raises:
        UniqueConstraintViolation: If username or email already exists
    """

    async with await db_connection() as session:
        result = await session.execute(
            select(db_mapping.User).where(
                db_mapping.User.email == email,
            )
        )

    if result.scalar_one_or_none():
        raise UniqueConstraintViolation("E-mail already in use")

    return True


@USER_ROUTER.post("/register")
async def handle_register_req(
    user: schemas.UserRegister, bg_tasks: BackgroundTasks
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
    """
    try:
        validate_email(user.email, check_deliverability=True)
    except EmailNotValidError:
        raise InvalidCredentials("Invalid E-mail")

    await search_for_user(email=user.email)

    bg_tasks.add_task(save_register_protocol, user=user)

    return Response("Verification mail sent successfully!")


@USER_ROUTER.get("/register/confirm/{protocol}")
async def handle_register_confirm_req(
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
        token_service (TokenService): Service for token operations (injected by FastAPI)
        session (AsyncSession): Database session (injected by FastAPI)

    Returns:
        TemplateResponse: Registration confirmation page with tokens

    Raises:
        InvalidProtocol: If protocol is invalid/expired
        UniqueConstraintViolation: If username/email became taken
    """

    async with redis_connection() as redis:
        user_data = await redis.hgetall(f"protocol:{protocol};type:register")

        if not user_data:
            raise InvalidProtocol()

        user_data["password"] = HASHER.hash(user_data.get("password"))

        try:
            created_user = await session.execute(
                insert(db_mapping.User)
                .values(user_data)
                .returning(db_mapping.User.user_id)
            )

        except exc.IntegrityError as e:
            if "uq_" in str(e):
                raise UniqueConstraintViolation("E-mail already in use")

        else:
            session_token = refresh_token = _generate_auth_tokens(
                created_user, token_service, False
            )

            token_service.set_refresh_token_cookie(
                token_service.response, refresh_token
            )

            await session.commit()

            redis.delete(f"protocol:{protocol};type:register")

            default_context = {
                "request": token_service.request,
                "token_type": "Bearer",
                "expires_in": int(Config.JWT_ACCESS_TOKEN_EXPIRES.total_seconds()),
            }

            return Jinja2Templates("./templates").TemplateResponse(
                name="confirm_register.html",
                context=default_context,
                headers={"Authorization": f"Bearer {session_token}"},
            )


@USER_ROUTER.post("/login")
async def handle_user_login_req(
    user: schemas.UserLogin,
    session: AsyncSession = Depends(db_connection),
    token_service: TokenService = Depends(TokenService),
) -> dict[str, Any]:
    """
    Verify user credentials and generate authentication tokens.
    This function:
    1. Checks if the user exists in the database
    2. Verifies the password
    3. Generates session and refresh tokens
    4. Sets the refresh token cookie
    Args:
        user (schemas.UserLogin): User login data
        session (AsyncSession): Database session (injected by FastAPI)
        token_service (TokenService): Token service instance (injected by FastAPI)
    Returns:
        dict[str, Any]: Authentication tokens and their metadata
    Raises:
        InvalidCredentials: If email format is invalid or credentials are incorrect
    """

    async with session:
        result = await session.execute(
            select(db_mapping.User.user_id, db_mapping.User.password).where(
                db_mapping.User.email == user.email,
            )
        )
        if not (found := result.first()):
            raise InvalidCredentials("User not found")

        try:
            HASHER.verify(found.password, user.password)
        except VerifyMismatchError:
            raise InvalidCredentials("Invalid password")

        session_token, refresh_token = await _generate_auth_tokens(
            user_id=found.user_id,
            token_service=token_service,
            long_session=user.keep_login,
        )

        await token_service.set_refresh_token_cookie(
            token_service.response, refresh_token
        )

        return Response(
            content={
                "message": "Login successful!",
                "token_type": "Bearer",
                "expires_in": int(token_service.session_expires.total_seconds()),
            },
            headers={"Authorization": f"Bearer {session_token}"},
        )


@USER_ROUTER.post("/logout")
async def handle_user_logout_req(
    token_service: TokenService = Depends(TokenService),
) -> dict[str, str]:
    """
    Logout user by deleting the refresh token cookie.
    Args:
        token_service (TokenService): Token service instance (injected by FastAPI)
    Returns:
        dict[str, str]: Success message indicating logout completion
    """
    token_service.delete_refresh_token_cookie(token_service.response)

    return Response("Logout completed successfully!")


@USER_ROUTER.post("/password_change")
async def handle_pwd_change_req(
    background_tasks: BackgroundTasks, user: schemas.UserPwdChange
):
    """
    Handle password change request by sending verification email.
    """
    background_tasks.add_task(save_pwd_change_protocol, user=user)
    return Response("Verification mail send successfully!")


@USER_ROUTER.get("/password_change/confirm/{protocol}")
async def handle_pwd_change_confirm_req(protocol: UUID):
    """
    This function confirms the password change by verifying the protocol.

    args:
        protocol (UUID): The protocol for the password change.

    returns:
        dict[str, str]: A message indicating the success of the password change.

    raises:
        InvalidProtocol: If the protocol is invalid or expired.
    """

    async with redis_connection() as redis:
        user_data = await redis.hgetall(f"protocol:{protocol};type:pwd_change")

        if not user_data:
            raise InvalidProtocol()

        new_hashed_pwd = HASHER.hash(user_data.new_password)

        try:
            async with await db_connection() as session:
                await session.execute(
                    update(db_mapping.User.password)
                    .where(db_mapping.User.email == user_data.email)
                    .values(new_hashed_pwd)
                )
                await session.commit()

        except exc.IntegrityError as e:
            if "uq_" in str(e):
                raise UniqueConstraintViolation("E-mail already in use")

        redis.delete(f"protocol:{protocol};type:pwd_change")

        return Response("Password changed successfully!")


@USER_ROUTER.post("/refresh_token")
async def handle_refresh_token_req(
    token_service: TokenService = Depends(TokenService),
) -> dict[str, str]:
    """
    Refresh user session token.

    This function checks the validity of the refresh token and generates a new session token.
    Args:
        token_service (TokenService): Token service instance (injected by FastAPI)
    Returns:
        dict[str, str]: New session token and its metadata
    """

    new_token = await token_service.renew_token(token_service.request)

    return Response(
        content={
            "message": "Token refreshed successfully!",
            "token_type": "Bearer",
            "expires_in": int(token_service.session_expires.total_seconds()),
        },
        headers={"Authorization": f"Bearer {new_token}"},
    )

@USER_ROUTER.get("/validate_token")
async def handle_validate_token_req(
    token_service: TokenService = Depends(TokenService),
) -> dict[str, str]:
    """
    Validate the current session token.

    This function checks if the session token is valid and returns its metadata.
    Args:
        token_service (TokenService): Token service instance (injected by FastAPI)
    Returns:
        dict[str, str]: Metadata about the session token
    """
    return Response(
        content={
            "message": "Token is valid",
            "token_type": "Bearer",
            "expires_in": int(token_service.session_expires.total_seconds()),
        }
    ) 
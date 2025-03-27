from datetime import datetime, timedelta, timezone
from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR, UNAUTHORIZED

import jwt
from database.utils import get_user_id_by_email
from fastapi import HTTPException, Request, Response
from pydantic import EmailStr

from core.config import Config
from core.exceptions import MissingToken, InvalidToken, SessionExpired, UnknownAuthError

async def generate_refresh_token(id_or_email: str | EmailStr) -> str:
    """Retorna um token JWT válido por 7 dias"""
    now = datetime.now(timezone.utc)

    if isinstance(id_or_email, EmailStr):
        id_or_email = await get_user_id_by_email(id_or_email)

    return jwt.encode(
        payload={"sub": str(id_or_email), "exp": now + timedelta(days=7)},
        key=Config.JWT_REFRESH_KEY,
        algorithm="HS256",
    )


async def generate_session_token(id_or_email: str | EmailStr) -> str:
    """Retorna um token JWT válido pelo tempo definido"""

    if isinstance(id_or_email, EmailStr):
        id_or_email = await get_user_id_by_email(id_or_email)

    now = datetime.now(timezone.utc)
    return jwt.encode(
        payload={
            "sub": str(id_or_email),
            "exp": now + timedelta(minutes=60),
        },
        key=Config.JWT_SESSION_KEY,
        algorithm="HS256",
    )

async def set_session_token_cookie(response: Response, token: str):
    exp = datetime.now(timezone.utc) + timedelta(hours=1)
    response.set_cookie(
        key="session_token",
        value=token,
        max_age=3600,  # 1 hora em segundos
        expires=exp,
        httponly=True,
        samesite="strict",
    )


async def set_refresh_token_cookie(response: Response, token: str):
    exp = datetime.now(timezone.utc) + timedelta(days=7)
    response.set_cookie(
        key="refresh_token",
        value=token,
        max_age=604800,  # 7 dias em segundos
        expires=exp,
        httponly=True,
        samesite="strict",
    )


async def get_session_token(request: Request, response: Response):
    token = request.cookies.get("session_token")

    if token is not None:
        return token
    else:
        return await renew_token(request, response)


def get_refresh_token(request: Request):
    token = request.cookies.get("refresh_token")

    if token:
        return token
    else:
        raise MissingToken("Refresh token não encontrado")


async def renew_token(request: Request, response: Response):
    token = get_refresh_token(request)

    try:
        decoded = jwt.decode(token, Config.JWT_REFRESH_KEY, algorithms=["HS256"])

    except jwt.exceptions.ExpiredSignatureError:
        raise SessionExpired()

    except jwt.exceptions.InvalidTokenError as e:
        raise InvalidToken()

    else:
        token = await generate_session_token(decoded["sub"])
        await set_session_token_cookie(response, token)
        return token


async def validate_token(request: Request, response: Response) -> int:
    try:
        token = await get_session_token(request, response)
        decoded = jwt.decode(token, Config.JWT_SESSION_KEY, algorithms="HS256")

    except jwt.exceptions.ExpiredSignatureError as e:
        raise SessionExpired()

    except jwt.exceptions.InvalidTokenError as e:
        raise InvalidToken()

    except jwt.DecodeError as e:
        raise UnknownAuthError()
    else:
        return int(decoded["sub"])

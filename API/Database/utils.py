from datetime import datetime, timedelta, timezone
from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR, NOT_FOUND, UNAUTHORIZED

import jwt
from Database import db_mapping as tables
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import EmailStr
from redis import Redis
from sqlalchemy import create_engine, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

JWT_REFRESH_KEY = "hlNDvdGkE69LAuM"
JWT_SESSION_KEY = "6TjFvAtLBhKOMoF"

oauth2_scheme = OAuth2PasswordBearer("/user/login")

ENGINE = create_engine(
    "postgresql://fortify_user:sXw8PMhZV0IPVgujiqI0LtlDgY7qTaXt@dpg-cuv5vs5umphs73f8qg00-a.oregon-postgres.render.com/fortify"
)

ASYNC_ENGINE = create_async_engine(
    "postgresql+asyncpg://fortify_user:sXw8PMhZV0IPVgujiqI0LtlDgY7qTaXt@dpg-cuv5vs5umphs73f8qg00-a.oregon-postgres.render.com/fortify"
)

Session = sessionmaker(ENGINE, autoflush=False)

AsyncSession = async_sessionmaker(ASYNC_ENGINE, autoflush=False)


def redis_pool():
    return Redis(
    host='redis-19517.c308.sa-east-1-1.ec2.redns.redis-cloud.com',
    port=19517,
    decode_responses=True,
    username="default",
    password="zkrynW67tEbFKRvvDQQc60UlPJz1kvwu",
)


async def get_user_id_by_email(user_email: EmailStr):
    async with AsyncSession() as session:
        result = await session.scalars(
            select(tables.Usuario.id_usuario).where(tables.Usuario.email == user_email)
        )
        try:
            return str(result.one())
        except NoResultFound:
            raise HTTPException(NOT_FOUND, "Não existe usuário com esse email")


async def generate_refresh_token(id_or_email: str | EmailStr) -> str:
    """Retorna um token JWT válido por 7 dias"""
    now = datetime.now(timezone.utc)

    if isinstance(id_or_email, EmailStr):
        id_or_email = await get_user_id_by_email(id_or_email)

    return jwt.encode(
        payload={"sub": str(id_or_email), "exp": now + timedelta(days=7)},
        key=JWT_REFRESH_KEY,
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
            "exp": now + timedelta(seconds=1),
        },
        key=JWT_SESSION_KEY,
        algorithm="HS256",
    )


def generate_register_token(email: EmailStr):
    now = datetime.now(timezone.utc)
    return jwt.encode(
        payload={
            "sub": email,
            "exp": now + timedelta(days=1),
        },
        key=JWT_SESSION_KEY,
        algorithm="HS256",
    )


def validate_token(token: str = Depends(oauth2_scheme)) -> int:
    try:
        decoded = jwt.decode(token, JWT_SESSION_KEY, algorithms="HS256")
    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException(UNAUTHORIZED, f"Token expirado, msg: {e}")
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(BAD_REQUEST, f"Token inválido, msg: {e}")
    except jwt.DecodeError as e:
        raise HTTPException(
            INTERNAL_SERVER_ERROR, f"Erro desconhecido validando token, msg: {e}"
        )
    else:
        return int(decoded["sub"])

from datetime import datetime, timedelta, timezone

import jwt
from Database import db_mapping as tables
from fastapi import HTTPException, Request
from pydantic import EmailStr
from redis import Redis
from sqlalchemy import create_engine, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound

JWT_REFRESH_KEY = "hlNDvdGkE69LAuM"
JWT_SESSION_KEY = "6TjFvAtLBhKOMoF"


ENGINE = create_engine("postgresql://lcsouza:Souza_0134@localhost/treino")

ASYNC_ENGINE = create_async_engine(
    "postgresql+asyncpg://lcsouza:Souza_0134@localhost/treino"
)

Session = sessionmaker(ENGINE, autoflush=False)

AsyncSession = async_sessionmaker(ASYNC_ENGINE, autoflush=False)


def redis_pool():
    return Redis(decode_responses=True)


async def get_user_id_by_email(user_email: EmailStr):

    async with AsyncSession() as session:
        result = await session.scalars(
            select(tables.Usuario.id_usuario).where(tables.Usuario.email == user_email)
        )
        try:
            return result.one()
        except NoResultFound:
            raise HTTPException(404, "Não existe usuário com esse email")


async def generate_refresh_token(id_or_email: int | EmailStr) -> str:
    """Retorna um token JWT válido por 7 dias"""
    now = datetime.now(timezone.utc)

    if isinstance(id_or_email, EmailStr):
        user_id = await get_user_id_by_email(id_or_email)

    return jwt.encode(
        payload={"sub": id_or_email, "exp": now + timedelta(days=7)},
        key=JWT_REFRESH_KEY,
    )


async def generate_session_token(id_or_email: int | EmailStr) -> str:
    """Retorna um token JWT válido pelo tempo definido"""

    if isinstance(id_or_email, EmailStr):
        id_or_email = await get_user_id_by_email(id_or_email)

    now = datetime.now(timezone.utc)
    return jwt.encode(
        payload={
            "sub": id_or_email,
            "exp": now + timedelta(minutes=30),
        },
        key=JWT_SESSION_KEY,
    )

async def generate_register_token(email: EmailStr):
    now = datetime.now(timezone.utc)
    return jwt.encode(
        payload={
            "sub": email,
            "exp": now + timedelta(days=1),
        },
        key=JWT_SESSION_KEY,
    )

def validate_token(request: Request):
    try:
        token = request.headers.get("authorization")
        assert token is not None
    except AssertionError:
        raise HTTPException(400, "Token não recebido")

    try:
        jwt.decode(token, JWT_SESSION_KEY)
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(401, "Token expirado")
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(400, "Token inválido")
    except jwt.DecodeError:
        raise HTTPException(500, "Erro desconhecido validando token")
    else:
        return True

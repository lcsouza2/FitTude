from datetime import timedelta
from pydantic import EmailStr

import jwt
from redis import Redis
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

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


def generate_refresh_token(id: int) -> str:
    """Retorna um token JWT válido por 7 dias"""
    return jwt.encode(payload={"sub": id, "exp": timedelta(7)}, key=JWT_REFRESH_KEY)


def generate_session_token(id_or_email: int | EmailStr, expire_in_a_day: bool = False) -> str:
    """Retorna um token JWT válido pelo tempo definido"""
    return jwt.encode(
        payload={
            "sub": id,
            "exp": timedelta(days=1) if expire_in_a_day else timedelta(minutes=30),
        },
        key=JWT_SESSION_KEY,
    )

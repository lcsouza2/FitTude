from http.client import NOT_FOUND

from database import db_mapping as tables
from fastapi import HTTPException
from pydantic import EmailStr
from redis import Redis
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

ASYNC_ENGINE = create_async_engine(
    # "postgresql+asyncpg://fortify_user:sXw8PMhZV0IPVgujiqI0LtlDgY7qTaXt@dpg-cuv5vs5umphs73f8qg00-a.oregon-postgres.render.com/fortify"
    "postgresql+asyncpg://lcsouza:Souza_0134@localhost:5432/treino"
)

AsyncSession = async_sessionmaker(ASYNC_ENGINE, autoflush=False)


def redis_pool():
    return Redis(
        # host="redis-19517.c308.sa-east-1-1.ec2.redns.redis-cloud.com",
        # port=19517,
        # decode_responses=True,
        # username="default",
        # password="zkrynW67tEbFKRvvDQQc60UlPJz1kvwu",
    )


async def get_user_id_by_email(email_usuario: EmailStr):
    async with AsyncSession() as session:
        result = await session.scalars(
            select(tables.Usuario.id_usuario).where(
                tables.Usuario.email == email_usuario
            )
        )
        try:
            return str(result.one())
        except NoResultFound:
            raise HTTPException(NOT_FOUND, "Não existe usuário com esse email")


def exclude_falsy_from_dict(payload: dict):
    return {key: value for key, value in payload.items() if value}

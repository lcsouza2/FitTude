from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from redis import Redis
from typing import Callable
from functools import wraps
from contextlib import asynccontextmanager

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


@asynccontextmanager
async def get_db_session():
    session = AsyncSession()
    try:
        yield session
    finally:
        await session.close()

def db_operation(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with get_db_session() as session:
            return await func(*args, **kwargs, session=session)
    return wrapper

@asynccontextmanager
async def get_redis():
    redis = redis_pool()
    try:
        yield redis
    finally:
        await redis.close()

def redis_operation(func: Callable) -> Callable:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with get_redis() as redis:
            return await func(redis, *args, **kwargs)
    return wrapper
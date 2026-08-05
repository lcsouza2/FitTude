from fastapi import Depends
from typing_extensions import Annotated

from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from .config import SETTINGS

ASYNC_ENGINE = create_async_engine(SETTINGS.POSTGRES_URL, echo=True)

session_maker = async_sessionmaker(ASYNC_ENGINE, autoflush=False)

REDIS_POOL = ConnectionPool.from_url(SETTINGS.REDIS_URL, decode_responses=True)

async def db_connection():
    async with session_maker() as session:
        yield session

async def redis_connection():
    async with Redis(connection_pool=REDIS_POOL) as redis:
        yield redis

AsyncSessionInjector = Annotated[AsyncSession, Depends(db_connection)]
RedisInjector = Annotated[Redis, Depends(redis_connection)]
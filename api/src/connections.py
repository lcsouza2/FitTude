from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .config import Config

ASYNC_ENGINE = create_async_engine(Config.DATABASE_URL)

AsyncSession = async_sessionmaker(ASYNC_ENGINE, autoflush=False)

REDIS_POOL = ConnectionPool.from_url(Config.REDIS_URL, decode_responses=True)


def redis_connection():
    return Redis.from_pool(REDIS_POOL)


async def db_connection():
    connection = AsyncSession()
    return connection

import redis.connection
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from redis import Redis
import redis

ENGINE = create_engine("postgresql://lcsouza:Souza_0134@localhost/treino")

ASYNC_ENGINE = create_async_engine("postgresql+asyncpg://lcsouza:Souza_0134@localhost/treino")

Session = sessionmaker(ENGINE, autoflush=False)

AsyncSession = async_sessionmaker(ASYNC_ENGINE, autoflush=False)

RedisPoll = lambda: Redis(decode_responses=True)

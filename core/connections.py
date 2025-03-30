
from redis.asyncio import ConnectionPool, Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

ASYNC_ENGINE = create_async_engine(
    # "postgresql+asyncpg://fortify_user:sXw8PMhZV0IPVgujiqI0LtlDgY7qTaXt@dpg-cuv5vs5umphs73f8qg00-a.oregon-postgres.render.com/fortify"
    "postgresql+asyncpg://lcsouza:Souza_0134@localhost:5432/treino"
)

AsyncSession = async_sessionmaker(ASYNC_ENGINE, autoflush=False)

REDIS_POOL = ConnectionPool.from_url("redis://localhost:6379", decode_responses=True)
# host="redis-19517.c308.sa-east-1-1.ec2.redns.redis-cloud.com",
# port=19517,
# decode_responses=True,
# username="default",
# password="zkrynW67tEbFKRvvDQQc60UlPJz1kvwu"


def redis_connection():
    return Redis.from_pool(REDIS_POOL)


def db_connection():
    connection = AsyncSession()
    return connection

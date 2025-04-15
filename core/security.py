from fastapi import Request

from core.config import Config 
from core.connections import redis_connection
from core.exceptions import RequestLimitExceeded

async def is_rate_limited(request: Request) -> bool:
    async with redis_connection() as redis:
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        current = await redis.get(key)

        if not current:
            await redis.setex(key, Config.REQUEST_TIME_WINDOW, 1)
            return False

        if int(current) >= Config.MAX_REQUESTS:
            raise RequestLimitExceeded()

        await redis.incr(key)
        return False

async def verify_request_limit(request: Request):
    await is_rate_limited(request)

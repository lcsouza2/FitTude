from fastapi import Request

from core.config import Config
from core.connections import redis_pool
from core.exceptions import RequestLimitExceeded


def is_rate_limited(request: Request) -> bool:
    with redis_pool() as redis:
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        current = redis.get(key)

        if not current:
            redis.setex(key, Config.REQUEST_TIME_WINDOW, 1)
            return False

        if int(current) >= Config.MAX_REQUESTS:
            raise RequestLimitExceeded()

        redis.incr(key)
        return False

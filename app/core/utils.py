from datetime import datetime, timezone
from functools import wraps
from json import dumps
from typing import Callable

from core.config import Config
from core.connections import redis_connection


def actual_datetime():
    return datetime.now(timezone.utc)


def exclude_falsy_from_dict(payload: dict):
    return {
        key: value for key, value in payload.items() if value or isinstance(value, bool)
    }


def cached_operation(timeout: int = Config.CACHE_DEFAULT_TIMEOUT):
    def decorator(
        func: Callable,
    ):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with redis_connection() as redis:
                parameters = dumps({"args": args, "kwargs": kwargs}, sort_keys=True)

                key = f"{func.__name__}:{parameters}"
                result = await redis.get(key)

                if result:
                    return result

                result = await func(*args, **kwargs)
                await redis.setex(key, timeout, str(result))
                return result

        return wrapper

    return decorator

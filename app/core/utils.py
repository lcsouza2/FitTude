from datetime import datetime, timezone
from functools import wraps
from json import dumps
from typing import Callable
import random 
import string

from app.core.config import Config
from app.core.connections import redis_connection


def actual_datetime():
    return datetime.now(timezone.utc).replace(microsecond=0)


def exclude_falsy_from_dict(payload: dict):
    return {
        key: value
        for key, value in payload.items()
        if value or (isinstance(value, bool) and value is True)
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

def generate_random_protocol(char_amount: int = 6):
    """
    Generate a random char alphanumeric string as a protocol.
    This protocol is used for password change requests.
    Args:
        char_amount (int): Number of characters in the protocol string. Default is 6.
    Returns:
        str: Randomly generated protocol string
    """

    return "".join(
        [random.choice(string.ascii_letters + string.digits) for _ in range(6)]
    )
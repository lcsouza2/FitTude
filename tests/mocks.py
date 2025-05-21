from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.database.db_mapping import reg


@pytest.fixture
def mock_uuid():
    """
    Fixture to mock the uuid4 function.
    This mock will replace the actual function with a MagicMock instance.
    The mock instance will return a specific uuid when called.
    """
    with patch("app.routes.user_routes.uuid4") as mock:
        mock.return_value = UUID("80e82bbc-9dee-424d-aafb-7559bcac15e5")
        yield mock


@pytest.fixture
def mock_char_protocol():
    """
    Fixture to mock the generate_random_protocol function.
    This mock will replace the actual function with a MagicMock instance.
    The mock instance will return a specific string when called.
    """
    with patch("app.routes.user_routes.generate_random_protocol") as mock:
        mock.return_value = "ab@123"
        yield mock


@pytest.fixture
def mock_redis():
    """
    Fixture to mock the Redis connection.
    This mock will replace the actual Redis connection with an AsyncMock instance.
    The mock instance will have its hset and expire methods replaced with AsyncMock instances.
    This allows you to test the behavior of your code without needing a real Redis instance.
    """
    redis_instance = AsyncMock()
    redis_instance.hset = AsyncMock()
    redis_instance.expire = AsyncMock()

    context_manager = AsyncMock()
    context_manager.__aenter__.return_value = redis_instance
    context_manager.__aexit__.return_value = None

    return (redis_instance, context_manager)


@pytest.fixture
def mock_email_client():
    """
    Fixture to mock the EmailClient class.
    This mock will replace the actual EmailClient with a MagicMock instance.
    The mock instance will have its send_register_verify_mail and send_pwd_change_mail methods
    replaced with AsyncMock instances.
    This allows you to test the behavior of your code without sending actual emails.
    """

    with patch("app.routes.user_routes.EmailClient") as mock_email:
        email_instance = MagicMock()
        email_instance.send_register_verify_mail = AsyncMock()
        email_instance.send_pwd_change_mail = AsyncMock()
        mock_email.return_value = email_instance
        yield email_instance


class MockDatabase:
    def __init__(self):
        self.engine = create_async_engine("sqlite+aiosqlite:///:memory:")

        self.connection = None
        self.session_factory = None

    async def __aenter__(self):
        self.connection = await self.engine.connect()
        await self.connection.run_sync(reg.metadata.create_all)

        self.session_factory = async_sessionmaker(
            bind=self.connection, expire_on_commit=False
        )
        return self.session_factory()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.connection.close()

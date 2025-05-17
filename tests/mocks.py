import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine

@pytest.fixture
def mock_uuid():
    with patch("app.routes.user_routes.uuid4") as mock:
        mock.return_value = UUID("80e82bbc-9dee-424d-aafb-7559bcac15e5")
        yield mock

@pytest.fixture
def mock_char_protocol():
    with patch("app.routes.user_routes.generate_random_protocol") as mock:
        mock.return_value = "ab@123"
        yield mock

@pytest.fixture
def mock_redis():
    redis_instance = AsyncMock()
    redis_instance.hset = AsyncMock()
    redis_instance.expire = AsyncMock()
    
    context_manager = AsyncMock()
    context_manager.__aenter__.return_value = redis_instance
    context_manager.__aexit__.return_value = None

    with patch('app.routes.user_routes.redis_connection', return_value=context_manager):
        yield redis_instance

@pytest.fixture
def mock_email_client():
    with patch('app.routes.user_routes.EmailClient') as mock_email:
        email_instance = MagicMock()
        email_instance.send_register_verify_mail = AsyncMock()
        email_instance.send_pwd_change_mail = AsyncMock()
        mock_email.return_value = email_instance
        yield email_instance

@pytest.fixture
def mock_database():
    session_maker = async_sessionmaker(AsyncEngine("sqlite+aiosqlite:///:memory:"))
    session = AsyncSession(session_maker)
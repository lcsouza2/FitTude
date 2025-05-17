from app.routes.user_routes import USER_ROUTER, save_pwd_change_protocol, save_register_protocol, UUID
from unittest.mock import AsyncMock, patch, MagicMock
from app.core.schemas import UserRegister
import pytest

@pytest.fixture
def mock_uuid():
    with patch("app.routes.user_routes.uuid4") as mock:
        mock.return_value = UUID("80e82bbc-9dee-424d-aafb-7559bcac15e5")
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
        email_instance.send_password_change_mail = AsyncMock()
        mock_email.return_value = email_instance
        yield email_instance


@pytest.mark.asyncio
async def test_save_register_protocol(
    mock_uuid, mock_redis, mock_email_client
):

    fake_user = UserRegister(
        email="randomuser@gmail.com",
        name="Random User",
        password="RandomPassword"
    )
    protocol_key = f"protocol:{mock_uuid.return_value};type:register"

    await save_register_protocol(fake_user)

    mock_email_client.send_register_verify_mail.assert_called_once_with(
        dest_email=fake_user.email,
        protocol=mock_uuid.return_value,
        username=fake_user.name.split()[0],
    )

    mock_redis.hset.assert_called_once_with(
        protocol_key,
        mapping=fake_user.model_dump(),
    )

    mock_redis.expire.assert_called_once_with(
        protocol_key,
        1800,
    )

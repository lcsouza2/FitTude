from app.routes.user_routes import USER_ROUTER, save_pwd_change_protocol, save_register_protocol, UUID
from app.core.schemas import UserRegister
import pytest
from fastapi.testclient import TestClient
from ..mocks import mock_uuid, mock_char_protocol, mock_redis, mock_email_client

fastapi_test_client = TestClient(USER_ROUTER)


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

@pytest.mark.asyncio
async def test_save_pwd_change_protocol(
    mock_char_protocol, mock_redis, mock_email_client
):

    fake_user = UserRegister(
        email="randomuser@gmail.com",
        name="Random User",
        password="RandomPassword"
    )
    protocol_key = f"protocol:{mock_char_protocol.return_value};type:pwd_change"

    await save_pwd_change_protocol(fake_user)

    mock_email_client.send_pwd_change_mail.assert_called_once_with(
        dest_email=fake_user.email,
        char_protocol=mock_char_protocol.return_value,
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

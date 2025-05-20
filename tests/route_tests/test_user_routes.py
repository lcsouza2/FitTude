from app.routes import user_routes
from app.core.schemas import UserRegister
import pytest
from fastapi.testclient import TestClient
from ..mocks import *
from unittest.mock import patch

fastapi_test_client = TestClient(user_routes.USER_ROUTER)


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

    with patch('app.routes.user_routes.redis_connection', return_value=mock_redis[1]):
        await user_routes.save_register_protocol(fake_user)

        mock_redis[0].hset.assert_called_once_with(
            protocol_key,
            mapping=fake_user.model_dump(),
        )

        mock_redis[0].expire.assert_called_once_with(
            protocol_key,
            1800,
        )

    mock_email_client.send_register_verify_mail.assert_called_once_with(
        dest_email=fake_user.email,
        protocol=mock_uuid.return_value,
        username=fake_user.name.split()[0],
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

    with patch('app.routes.user_routes.redis_connection', return_value=mock_redis[1]):

        await user_routes.save_pwd_change_protocol(fake_user)

        mock_redis[0].hset.assert_called_once_with(
            protocol_key,
            mapping=fake_user.model_dump(),
        )

        mock_redis[0].expire.assert_called_once_with(
            protocol_key,
            1800,
        )

    mock_email_client.send_pwd_change_mail.assert_called_once_with(
        dest_email=fake_user.email,
        char_protocol=mock_char_protocol.return_value,
        username=fake_user.name.split()[0],
    )

async def test_search_for_user_return_true():



    with patch("app.routes.user_routes.db_connection",new_callable=setup_db_conn) as mock:
        await user_routes.search_for_user("test_mail@gmail.com") == True




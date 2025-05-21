from app.routes import user_routes
from app.core.schemas import UserRegister
import pytest
from fastapi.testclient import TestClient
from ..mocks import *
from unittest.mock import patch
from sqlalchemy import insert
from app.database import db_mapping
from app.core.exceptions import UniqueConstraintViolation, InvalidCredentials
from app.core import schemas
from app.main import MAIN_APP

fastapi_test_client = TestClient(MAIN_APP)


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
    """
    This test simulate the original function behavior
    """

    mock_database = MockDatabase()

    fake_user = db_mapping.User(
        name="Random User",
        email="test_email@gmail.com",
        password="hashedpassword",
    )

    async with mock_database as conn:
        with patch("app.routes.user_routes.db_connection", return_value=conn):
            await conn.execute(
                insert(db_mapping.User).values(
                    name=fake_user.name,
                    email=fake_user.email,
                    password=fake_user.password
                )
            )
            await conn.commit()

            assert await user_routes.search_for_user("non_existing_email@gmail.com") is True

            with pytest.raises(UniqueConstraintViolation):
                assert await user_routes.search_for_user(fake_user.email) is True


def test_handle_register_req():
    fake_user = schemas.UserRegister(
        email="test_mail@gmail.com",
        password="test_password",
        name="Test User"
    )
    
    response = fastapi_test_client.post("/api/user/register", json=fake_user.model_dump())

    assert response.status_code == 200

    fake_user.email = "Non-valid@email.com"
    with pytest.raises(InvalidCredentials):
        response = fastapi_test_client.post("/api/user/register", json=fake_user.model_dump())
        print(response)
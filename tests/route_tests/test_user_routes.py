from fastapi.testclient import TestClient
from app.routes.user_routes import USER_ROUTER, save_pwd_change_protocol, search_for_user, save_register_protocol
from unittest.mock import patch, MagicMock
from app.core import schemas


test_client = TestClient(USER_ROUTER)

@patch("app.core.email_service.FastMail.send_message")
@patch("app.core.connections.redis_connection")
async def test_save_register_protocol(
    patched_email_client: MagicMock, 
    patched_redis: MagicMock
    ):


    await save_register_protocol(schemas.UserRegister(
        email="lcsouzagarcia@gmail.com", 
        password="senha", 
        name="Luiz Souza Garcia"
            )
        )

    patched_email_client.assert_called_once()

    redis_instance.hset.assert_called_once() 


def test_create_user():
    test_client.post("/api/user/")
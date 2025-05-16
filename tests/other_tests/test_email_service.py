from unittest.mock import patch, MagicMock
from uuid import uuid4
from app.core.email_service import EmailClient


@patch("app.core.email_service.FastMail.send_message")
async def test_send_pwd_change_mail(send_message_mock: MagicMock):
    instance = send_message_mock.return_value

    call_result = await EmailClient().send_pwd_change_mail(
        "lcsouzagarcia@gmail.com", "Luiz", 123456
    )

    send_message_mock.assert_called_once()

    assert call_result is True


@patch("app.core.email_service.FastMail.send_message")
async def test_send_register_verify_mail(send_message_mock: MagicMock):
    instance = send_message_mock.return_value

    call_result = await EmailClient().send_register_verify_mail(
        "lcsouzagarcia@gmail.com", uuid4(), "Luiz"
    )

    send_message_mock.assert_called_once()

    assert call_result is True

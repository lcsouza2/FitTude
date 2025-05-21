from unittest.mock import MagicMock, patch

from fastapi import Request, Response
from fastapi.security import HTTPAuthorizationCredentials
from jwt import encode
from pytest import raises

from app.core.authentication import TokenService
from app.core.exceptions import (
    InvalidToken,
    MissingToken,
)


class TestTokenService:
    def __init__(self):
        self.test_token = encode(
            payload={"sub": "1"},
            key="test_key",
        )

        self.cookies = {
            "invalid_refresh_token": "mock_refresh_token",
            "refresh_token": self.test_token,
        }

    def set_cookie(self, key, value, **args):
        self.cookies[key] = value

    def delete_cookie(self, key):
        if key in self.cookies:
            del self.cookies[key]


def token_service_factory():
    service = TokenService(
        request=MagicMock(spec=Request), response=MagicMock(spec=Response)
    )

    service.refresh_key = "test_key"
    service.session_key = "test_key"

    return service


token_service = lambda: token_service_factory()

custom_token_service = lambda: TestTokenService()


async def test_generate_refresh_token():
    """
    Test the generate_token function to ensure it correctly generates a token.
    """

    token = await token_service().generate_refresh_token(id=1)

    assert isinstance(token, str), "Token should be a string"
    assert len(token) > 0, "Token should not be empty"


async def test_generate_session_token():
    """
    Test the generate_token function to ensure it correctly generates a token.
    """

    token = await token_service().generate_session_token(id=1)

    assert isinstance(token, str), "Token should be a string"
    assert len(token) > 0, "Token should not be empty"


async def test_set_refresh_token_cookie():
    """
    Test the set_refresh_token_cookie function to ensure it correctly sets the refresh token cookie.
    """

    instance = custom_token_service()

    instance.cookies = {}

    await token_service().set_refresh_token_cookie(instance, "mock_refresh_token")

    assert instance.cookies == {"refresh_token": "mock_refresh_token"}


def test_get_refresh_token():
    """
    Test the get_refresh_token function to ensure it correctly retrieves the refresh token from cookies.
    """

    instance = custom_token_service()

    token = token_service().get_refresh_token(instance)

    assert token == instance.test_token

    with raises(MissingToken):
        instance.cookies.pop("refresh_token")
        token_service().get_refresh_token(instance)


def test_delete_refresh_token_cookie():
    """
    Test the delete_refresh_token_cookie function to ensure it correctly deletes the refresh token cookie.
    """

    instance = custom_token_service()

    instance.cookies.pop("invalid_refresh_token")

    token_service().delete_refresh_token_cookie(instance)

    assert instance.cookies == {}


async def test_renew_token():
    """
    Test the renew_token function to ensure it correctly generates a new session token.
    """

    instance = custom_token_service()

    token = await token_service().renew_token(instance)

    instance.cookies = {"refresh_token": instance.cookies["invalid_refresh_token"]}

    with raises(InvalidToken):
        await token_service().renew_token(instance)

    assert isinstance(token, str), "Token should be a string"
    assert len(token) > 0, "Token should not be empty"


@patch("app.core.config.Config.get_jwt_session_key", return_value="test_key")
async def test_validate_token(patched_key):
    """
    Test the validate_token function to ensure it correctly validates a token.
    """

    instance = custom_token_service()

    token = await token_service().validate_token(
        HTTPAuthorizationCredentials(scheme="Bearer", credentials=instance.test_token)
    )

    assert token == 1, "Token should be valid and return the user ID"

    with raises(MissingToken):
        await token_service().validate_token(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials="")
        )

    with raises(InvalidToken):
        await token_service().validate_token(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_token")
        )

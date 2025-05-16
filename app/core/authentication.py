import jwt
from fastapi import Depends, Request, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import Config
from app.core.exceptions import (
    InvalidToken,
    MissingToken,
    SessionExpired,
    UnknownAuthError,
)
from app.core.utils import actual_datetime


class TokenService:
    security = HTTPBearer()

    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response
        self.session_key = Config.get_jwt_session_key()
        self.refresh_key = Config.get_jwt_refresh_key()
        self.algorithm = Config.JWT_ALGORITHM
        self.session_expires = Config.JWT_ACCESS_TOKEN_EXPIRES
        self.refresh_expires = Config.JWT_REFRESH_TOKEN_EXPIRES

    async def generate_refresh_token(self, id: int) -> str:
        """
        Create a JWT refresh token with the user id and expiration time.
        Args:
            id (int): User ID to be included in the token payload.
        Returns:
            str: Encoded JWT refresh token.
        """

        return jwt.encode(
            payload={"sub": str(id), "exp": self.refresh_expires + actual_datetime()},
            key=self.refresh_key,
            algorithm=self.algorithm,
        )

    async def generate_session_token(self, id: int) -> str:
        """
        Create a JWT session token with the user id and expiration time.
        Args:
            id (int): User ID to be included in the token payload.
        Returns:
            str: Encoded JWT session token.
        """

        return jwt.encode(
            payload={
                "sub": str(id),
                "exp": self.session_expires + actual_datetime(),
            },
            key=self.session_key,
            algorithm=self.algorithm,
        )

    async def set_refresh_token_cookie(self, response: Response, token: str):
        """
        Sets the refresh token in the response cookies.
        Args:
            response (Response): The response object to set the cookie on.
            token (str): The refresh token to be set in the cookie.
        """

        response.set_cookie(
            key="refresh_token",
            value=token,
            max_age=Config.JWT_REFRESH_COOKIE_MAX_AGE,  # 7 dias em segundos
            expires=actual_datetime() + self.refresh_expires,
            httponly=True,
            secure=True,
            samesite="strict",
        )

    def get_refresh_token(self, request: Request) -> str:
        """
        Get the refresh token from the request cookies.
        Args:
            request (Request): The request object to get the cookie from.
        Returns:
            str: The refresh token from the request cookies.
        Raises:
            MissingToken: If the refresh token is not found in the cookies.
        """

        token = request.cookies.get("refresh_token")

        if token:
            return token
        else:
            raise MissingToken("Refresh token não encontrado")

    def delete_refresh_token_cookie(self, response: Response):
        """
        Deletes the refresh token cookie from the response. (like a logout action)
        Args:
            response (Response): The response object to delete the cookie from.
        """
        response.delete_cookie("refresh_token")

    async def renew_token(self, request: Request) -> str:
        """
        Gets the refresh token from the request and generates a new session token.
        Args:
            request (Request): The request object to get the refresh token from.
        Returns:
            str: The new session token.
        Raises:
            SessionExpired: If the refresh token has expired.
            InvalidToken: If the refresh token is invalid.
        """
        token = self.get_refresh_token(request)

        try:
            decoded = jwt.decode(token, self.refresh_key, algorithms=self.algorithm)

        except jwt.exceptions.ExpiredSignatureError:
            raise SessionExpired()

        except jwt.exceptions.InvalidTokenError:
            raise InvalidToken()

        else:
            token = await self.generate_session_token(decoded["sub"])
            return token

    @staticmethod
    async def validate_token(
        token: HTTPAuthorizationCredentials = Depends(security),
    ) -> int:
        """
        Validates the JWT token and returns the user ID.
        Args:
            token (HTTPAuthorizationCredentials): The JWT token to be validated.
        Returns:
            int: The user ID from the token payload.
        Raises:
            MissingToken: If the token is not found.
            SessionExpired: If the token has expired.
            InvalidToken: If the token is invalid.
            UnknownAuthError: If the token cannot be decoded.
        """

        token = token.credentials

        if not token:
            raise MissingToken("Refresh token não encontrado")

        try:
            decoded = jwt.decode(
                token,
                key=Config.get_jwt_session_key(),
                algorithms=Config.JWT_ALGORITHM,
            )

        except jwt.exceptions.ExpiredSignatureError:
            raise SessionExpired()

        except jwt.exceptions.InvalidTokenError:
            raise InvalidToken()

        except jwt.DecodeError:
            raise UnknownAuthError()
        else:
            return int(decoded["sub"])

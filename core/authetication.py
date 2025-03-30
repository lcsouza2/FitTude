import jwt
from fastapi import Depends, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from core.config import Config
from core.exceptions import InvalidToken, MissingToken, SessionExpired, UnknownAuthError
from core.utils import actual_datetime


class TokenService:
    security = HTTPBearer(auto_error=False)

    def __init__(self, request: Request, response: Response):
        self.request = request
        self.response = response
        self.session_key = Config.get_jwt_session_key()
        self.refresh_key = Config.get_jwt_refresh_key()
        self.algorithm = Config.JWT_ALGORITHM
        self.session_expires = Config.JWT_ACCESS_TOKEN_EXPIRES
        self.refresh_expires = Config.JWT_REFRESH_TOKEN_EXPIRES

    async def generate_refresh_token(self, id: int) -> str:
        """Retorna um token JWT válido por 7 dias"""

        return jwt.encode(
            payload={"sub": str(id), "exp": self.refresh_expires + actual_datetime()},
            key=self.refresh_key,
            algorithm=self.algorithm,
        )

    async def generate_session_token(self, id: int) -> str:
        """Retorna um token JWT válido pelo tempo definido"""

        return jwt.encode(
            payload={
                "sub": str(id),
                "exp": self.session_expires + actual_datetime(),
            },
            key=self.session_key,
            algorithm=self.algorithm,
        )

    async def set_refresh_token_cookie(self, response: Response, token: str):
        response.set_cookie(
            key="refresh_token",
            value=token,
            max_age=Config.JWT_REFRESH_COOKIE_MAX_AGE,  # 7 dias em segundos
            expires=actual_datetime() + self.refresh_expires,
            httponly=True,
            samesite="strict",
        )

    def get_refresh_token(self, request: Request):
        token = request.cookies.get("refresh_token")

        if token:
            return token
        else:
            raise MissingToken("Refresh token não encontrado")

    async def renew_token(self, request: Request):
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

    @classmethod
    async def validate_token(cls, token: HTTPAuthorizationCredentials = Depends(security)) -> int:
        """Valida o token JWT e retorna o id do usuário"""
        try:
            decoded = jwt.decode(
                token.credentials,
                Config.get_jwt_session_key(),
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

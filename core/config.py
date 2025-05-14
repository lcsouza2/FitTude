import os
from datetime import timedelta
from typing import Any
from dotenv import load_dotenv

class Config:
    # Application Settings
    APP_NAME: str = "FitTude"
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_URL: str = os.getenv("REDIS_URL")

    # Mail Settings
    MAIL_USERNAME: str = os.getenv("MAIL_USERNAME")
    __MAIL_PASSWORD: str = os.getenv("MAIL_PASSWORD")
    MAIL_PORT: int = 587
    _MAIL_SERVER: str = os.getenv("MAIL_SERVER")
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_FROM: str = os.getenv("MAIL_FROM")
    MAIL_FROM_NAME: str = "FitTude Team"

    # Authentication Settings
    AUTH_REQUIRED: bool = True
    PASSWORD_HASH_ALGORITHM: str = "argon2"
    PASSWORD_RESET_TIMEOUT: timedelta = timedelta(hours=24)
    REGISTER_CONFIRM_TIMEOUT: timedelta = timedelta(minutes=30)
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_TIME: timedelta = timedelta(minutes=15)

    # JWT Settings
    __JWT_REFRESH_KEY: str = os.getenv("JWT_REFRESH_KEY")
    __JWT_SESSION_KEY: str = os.getenv("JWT_SESSION_KEY")
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=7)
    JWT_REFRESH_COOKIE_MAX_AGE: int = 604800  # 7 days in seconds
    JWT_ALGORITHM: str = "HS256"
    JWT_HEADER_TYPE: str = "Bearer"
    JWT_HEADER_NAME: str = "Authorization"
    JWT_BLACKLIST_ENABLED: bool = True
    JWT_BLACKLIST_TOKEN_CHECKS: set[str] = {"access", "refresh"}

    # Security Settings
    CORS_ORIGINS: list[str] = ["http://localhost:8000", "https://fittude.onrender.com"]
    ALLOWED_HOSTS: list[str] = ["localhost", "fittude.com"]
    MAX_REQUESTS: int = 100
    REQUEST_TIME_WINDOW: timedelta = timedelta(minutes=1)

    CACHE_DEFAULT_TIMEOUT: int = 300  # 5 minutes

    # Pagination Settings
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 50

    @classmethod
    def get_mail_password(cls) -> str:
        """Get the mail password"""
        return cls.__MAIL_PASSWORD

    @classmethod
    def get_mail_server(cls) -> str:
        """Get the mail server address"""
        return cls._MAIL_SERVER

    @classmethod
    def get_jwt_refresh_key(cls) -> str:
        """Get the JWT refresh key"""
        return cls.__JWT_REFRESH_KEY

    @classmethod
    def get_jwt_session_key(cls) -> str:
        """Get the JWT session key"""
        return cls.__JWT_SESSION_KEY

    @classmethod
    def get_cache_redis_url(cls) -> str:
        """Get the Redis cache URL"""
        return cls._CACHE_REDIS_URL

    @classmethod
    def get_settings(cls) -> dict[str, Any]:
        """Return all public settings as a dictionary"""
        return {k: v for k, v in cls.__dict__.items() if not k.startswith("_")}

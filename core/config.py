import os
from datetime import timedelta
from typing import Any


class Config:
    # Application Settings
    APP_NAME: str = "FitTude"

    # Mail Settings
    MAIL_USERNAME: str = "fittude.gym@gmail.com"
    MAIL_PASSWORD: str = "ghwk qhez ovdr tofn"
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_FROM: str = "fittude.gym@gmail.com"
    MAIL_FROM_NAME: str = "FitTude Team"

    # Authentication Settings
    AUTH_REQUIRED: bool = True
    PASSWORD_HASH_ALGORITHM: str = "argon2"
    MIN_PASSWORD_LENGTH: int = 8
    PASSWORD_RESET_TIMEOUT: timedelta = timedelta(hours=24)
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_TIME: timedelta = timedelta(minutes=15)

    # JWT Settings
    JWT_REFRESH_KEY: str = os.getenv("JWT_REFRESH_KEY", "hlNDvdGkE69LAuM")
    JWT_SESSION_KEY: str = os.getenv("JWT_SESSION_KEY", "6TjFvAtLBhKOMoF")
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=30)
    JWT_ALGORITHM: str = "HS256"
    JWT_HEADER_TYPE: str = "Bearer"
    JWT_HEADER_NAME: str = "Authorization"
    JWT_BLACKLIST_ENABLED: bool = True
    JWT_BLACKLIST_TOKEN_CHECKS: set[str] = {"access", "refresh"}

    # Security Settings
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "https://fittude.com"]
    ALLOWED_HOSTS: list[str] = ["localhost", "fittude.com"]
    MAX_REQUESTS: int = 100
    REQUEST_WINDOW: timedelta = timedelta(minutes=1)

    # Session Settings
    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"

    # Cache Settings
    CACHE_TYPE: str = "redis"
    CACHE_REDIS_URL: str = "redis://localhost:63790"
    CACHE_DEFAULT_TIMEOUT: int = 300  # 5 minutes

    # Pagination Settings
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    @classmethod
    def get_settings(cls) -> dict[str, Any]:
        """Return all settings as a dictionary"""
        return {k: v for k, v in cls.__dict__.items() if not k.startswith("_")}

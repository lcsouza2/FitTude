from pydantic import Field
from datetime import timedelta
from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Application Settings
    APP_NAME: str = "OVERLOAD"
    ENVIRONMENT: str = "development"


    # Redis Settings
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    @property
    def REDIS_URL(self) -> str:
        """Get the Redis connection URL"""
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    # PostgreSQL Settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = Field(exclude=True)
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_TEST_DB: str

    @property
    def POSTGRES_URL(self) -> str:
        """Get the PostgreSQL connection URL"""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    @property
    def POSTGRES_TEST_URL(self) -> str:
        """Get the PostgreSQL test database connection URL"""
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_TEST_DB}"


    # Mail Settings
    MAIL_USERNAME: str
    MAIL_PASSWORD: str = Field(exclude=True)
    MAIL_PORT: int = 587
    MAIL_SERVER: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    MAIL_FROM: str
    MAIL_FROM_NAME: str = "OVERLOAD Team"


    # Authentication Settings
    AUTH_REQUIRED: bool = ENVIRONMENT == "production"
    PASSWORD_HASH_ALGORITHM: str = "argon2"
    PASSWORD_RESET_TIMEOUT: timedelta = timedelta(hours=24)
    REGISTER_CONFIRM_TIMEOUT: timedelta = timedelta(minutes=30)
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_TIME: timedelta = timedelta(minutes=15)


    # JWT Settings
    JWT_REFRESH_KEY: str = Field(exclude=True)
    JWT_SESSION_KEY: str = Field(exclude=True)
    JWT_ACCESS_TOKEN_EXPIRES: timedelta = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES: timedelta = timedelta(days=7)
    JWT_REFRESH_COOKIE_MAX_AGE: int = 604800  # 7 days in seconds
    JWT_ALGORITHM: str = "HS256"
    JWT_HEADER_TYPE: str = "Bearer"
    JWT_HEADER_NAME: str = "Authorization"


    # Security Settings
    CORS_ORIGINS: list[str] = ["*"] if ENVIRONMENT == "development" else []
    ALLOWED_HOSTS: list[str] = ["*"] if ENVIRONMENT == "development" else []
    MAX_REQUESTS: int = 100
    REQUEST_TIME_WINDOW: timedelta = timedelta(minutes=1)
    CACHE_DEFAULT_TIMEOUT: int = 300  # 5 minutes


    # Pagination Settings
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 50

SETTINGS = _Settings()
__all__ = ["SETTINGS"]
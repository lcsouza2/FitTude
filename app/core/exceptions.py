from http.client import (
    BAD_REQUEST,
    CONFLICT,
    INTERNAL_SERVER_ERROR,
    NOT_FOUND,
    TOO_MANY_REQUESTS,
    UNAUTHORIZED,
    UNPROCESSABLE_ENTITY,
)

from fastapi import HTTPException


class DatabaseError(HTTPException):
    """Base exception for database related errors."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class PrimaryKeyViolation(DatabaseError):
    """Raised when trying to insert a record with an existing primary key."""

    def __init__(self, message: str = "Primary key violation"):
        super().__init__(CONFLICT, message)


class UniqueConstraintViolation(DatabaseError):
    """Raised when a unique constraint is violated."""

    def __init__(self, message: str = "Unique constraint violation"):
        super().__init__(CONFLICT, message)


class ForeignKeyViolation(DatabaseError):
    """Raised when referenced entity does not exist."""

    def __init__(self, message: str = "Referenced entity not found"):
        super().__init__(NOT_FOUND, message)


class EntityNotFound(DatabaseError):
    """Raised when the requested entity does not exist."""

    def __init__(self, message: str = "Entity not found"):
        super().__init__(NOT_FOUND, message)


class MissingParameters(HTTPException):
    """Raised when required parameters are not sent"""

    def __init__(self, message: str = "Missing required parameters"):
        super().__init__(UNPROCESSABLE_ENTITY, message)


class AuthenticationError(HTTPException):
    """Base exception for authentication related errors."""

    def __init__(self, message: str, status_code: int = UNAUTHORIZED):
        super().__init__(status_code=status_code, detail=message)


class InvalidToken(AuthenticationError):
    """Raised when the provided token is invalid or expired."""

    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message)


class InvalidCredentials(AuthenticationError):
    """Raised when user provides invalid username or password."""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message)


class SessionExpired(AuthenticationError):
    """Raised when user session has expired."""

    def __init__(self, message: str = "Session expired. Please login again"):
        super().__init__(message)


class MissingToken(AuthenticationError):
    """Raised when authentication token is not provided."""

    def __init__(self, message: str = "Authentication token not provided"):
        super().__init__(message, status_code=BAD_REQUEST)


# Security errors
class RequestLimitExceeded(HTTPException):
    """Raised when the request limit has been exceeded."""

    def __init__(self, message: str = "Request limit exceeded"):
        super().__init__(status_code=TOO_MANY_REQUESTS, detail=message)


class InvalidProtocol(HTTPException):
    """Raised when the protocol is invalid or expired."""

    def __init__(self, message: str = "Invalid or expired protocol"):
        super().__init__(status_code=NOT_FOUND, detail=message)


# Server errors
class UnknownAuthError(HTTPException):
    """Raised when an unknown error occurs during authentication."""

    def __init__(self, message: str = "Unknown authentication error"):
        super().__init__(status_code=INTERNAL_SERVER_ERROR, detail=message)


class MailServiceError(HTTPException):
    """Raised when there is an error with the mail service."""

    def __init__(self, message: str = "Mail service error"):
        super().__init__(status_code=INTERNAL_SERVER_ERROR, detail=message)

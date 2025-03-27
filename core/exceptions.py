from http.client import CONFLICT, NOT_FOUND, TOO_MANY_REQUESTS, UNAUTHORIZED, INTERNAL_SERVER_ERROR, BAD_REQUEST
from fastapi import HTTPException


# Erros de banco de dados
class DatabaseError(HTTPException):
    """Base exception for database related errors."""

    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)


class PrimaryKeyViolation(DatabaseError):
    """Raised when trying to insert a record with an existing primary key."""

    def __init__(self, entity: str):
        super().__init__(CONFLICT, f"O(a) {entity} já existe")


class UniqueConstraintViolation(DatabaseError):
    """Raised when a unique constraint is violated."""

    def __init__(self, entity: str):
        super().__init__(CONFLICT, f"O(a) {entity} já existe")


class ForeignKeyViolation(DatabaseError):
    """Raised when referenced entity does not exist."""

    def __init__(self, entity: str):
        super().__init__(NOT_FOUND, f"O(a) {entity} referenciado não existe")


# Erros de autenticação do usuário
class AuthenticationError(HTTPException):
    """Base exception for authentication related errors."""

    def __init__(self, message: str, status_code:int = UNAUTHORIZED,):
        super().__init__(status_code=status_code, detail=message)


class InvalidToken(AuthenticationError):
    """Raised when the provided token is invalid or expired."""

    def __init__(self, message: str = "Token inválido ou expirado"):
        super().__init__(message)


class InvalidCredentials(AuthenticationError):
    """Raised when user provides invalid username or password."""

    def __init__(self, message: str = "Credenciais inválidas"):
        super().__init__(message)

class SessionExpired(AuthenticationError):
    """Raised when user session has expired."""

    def __init__(
        self, message: str = "Sessão expirada. Por favor, faça login novamente"
    ):
        super().__init__(message)


class MissingToken(AuthenticationError):
    """Raised when authentication token is not provided."""

    def __init__(self, message: str = "Token de autenticação não fornecido"):
        super().__init__(message, status_code=BAD_REQUEST)


# Security errors
class RequestLimitExceeded(HTTPException):
    """Raised when the request limit has been exceeded."""

    def __init__(self, message: str = "Limite de requisições excedido"):
        super().__init__(status_code=TOO_MANY_REQUESTS, detail=message)


#Server errors
class UnknownAuthError(HTTPException):
    """Raised when an unknown error occurs during authentication."""

    def __init__(self, message: str = "Erro desconhecido durante autenticação"):
        super().__init__(status_code=INTERNAL_SERVER_ERROR, detail=message)
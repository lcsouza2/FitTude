from fastapi import HTTPException
from http.client import NOT_FOUND, CONFLICT, UNAUTHORIZED

#Erros de banco de dados
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


#Erros de autenticação do usuário
class AuthenticationError(HTTPException):
    """Base exception for authentication related errors."""
    def __init__(self, message: str):
        super().__init__(status_code=UNAUTHORIZED, detail=message)

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
    def __init__(self, message: str = "Sessão expirada. Por favor, faça login novamente"):
        super().__init__(message)

class MissingToken(AuthenticationError):
    """Raised when authentication token is not provided."""
    def __init__(self, message: str = "Token de autenticação não fornecido"):
        super().__init__(message)
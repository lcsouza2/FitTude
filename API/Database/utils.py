from datetime import datetime, timedelta, timezone
from http.client import BAD_REQUEST, INTERNAL_SERVER_ERROR, NOT_FOUND, UNAUTHORIZED

import jwt
from Database import db_mapping as tables
from fastapi import HTTPException, Request, Response
from pydantic import EmailStr
from redis import Redis
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

JWT_REFRESH_KEY = "hlNDvdGkE69LAuM"
JWT_SESSION_KEY = "6TjFvAtLBhKOMoF"

ASYNC_ENGINE = create_async_engine(
    # "postgresql+asyncpg://fortify_user:sXw8PMhZV0IPVgujiqI0LtlDgY7qTaXt@dpg-cuv5vs5umphs73f8qg00-a.oregon-postgres.render.com/fortify"
    "postgresql+asyncpg://lcsouza:Souza_0134@localhost:5432/treino"
)

AsyncSession = async_sessionmaker(ASYNC_ENGINE, autoflush=False)


def redis_pool():
    return Redis(
        host="redis-19517.c308.sa-east-1-1.ec2.redns.redis-cloud.com",
        port=19517,
        decode_responses=True,
        username="default",
        password="zkrynW67tEbFKRvvDQQc60UlPJz1kvwu",
    )


async def get_user_id_by_email(user_email: EmailStr):
    async with AsyncSession() as session:
        result = await session.scalars(
            select(tables.Usuario.id_usuario).where(tables.Usuario.email == user_email)
        )
        try:
            return str(result.one())
        except NoResultFound:
            raise HTTPException(NOT_FOUND, "Não existe usuário com esse email")


async def generate_refresh_token(id_or_email: str | EmailStr) -> str:
    """Retorna um token JWT válido por 7 dias"""
    now = datetime.now(timezone.utc)

    if isinstance(id_or_email, EmailStr):
        id_or_email = await get_user_id_by_email(id_or_email)

    return jwt.encode(
        payload={"sub": str(id_or_email), "exp": now + timedelta(days=7)},
        key=JWT_REFRESH_KEY,
        algorithm="HS256",
    )


async def generate_session_token(id_or_email: str | EmailStr) -> str:
    """Retorna um token JWT válido pelo tempo definido"""

    if isinstance(id_or_email, EmailStr):
        id_or_email = await get_user_id_by_email(id_or_email)

    now = datetime.now(timezone.utc)
    return jwt.encode(
        payload={
            "sub": str(id_or_email),
            "exp": now + timedelta(minutes=60),
        },
        key=JWT_SESSION_KEY,
        algorithm="HS256",
    )


async def set_session_token_cookie(response: Response, token: str):
    exp = datetime.now(timezone.utc) + timedelta(hours=1)
    response.set_cookie(
        key="session_token",
        value=token,
        max_age=3600,  # 1 hora em segundos
        expires=exp,
        httponly=True,
        samesite="strict",
    )


async def set_refresh_token_cookie(response: Response, token: str):
    exp = datetime.now(timezone.utc) + timedelta(days=7)
    response.set_cookie(
        key="refresh_token",
        value=token,
        max_age=604800,  # 7 dias em segundos
        expires=exp,
        httponly=True,
        samesite="strict",
    )


async def renew_token(request: Request, response: Response):
    # Tenta decodificar o token
    token = get_refresh_token(request)

    try:
        decoded = jwt.decode(token, JWT_REFRESH_KEY, algorithms=["HS256"])

        # Se o refresh token estiver expirado ele levanta erro 401()
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(UNAUTHORIZED, "Token de renovação expirado")

        # Se o token extiver inválido (alterado no cliente) levanda o erro 400
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(BAD_REQUEST, f"Token inválido recebido, msg {e}")

        # Se não ocorrerem erros cria um novo token de sessão
    else:
        token = await generate_session_token(decoded["sub"])
        await set_session_token_cookie(response, token)
        return token


async def get_session_token(request: Request, response: Response):
    token = request.cookies.get("session_token")

    # if token is not None:
    #     return token
    # else:
    return await renew_token(request, response)


def get_refresh_token(request: Request):
    token = request.cookies.get("refresh_token")

    if token:
        return token
    else:
        raise HTTPException(UNAUTHORIZED, "Usuário não autenticado")


async def validate_token(request: Request, response: Response) -> int:
    try:
        token = await get_session_token(request, response)

        decoded = jwt.decode(token, JWT_SESSION_KEY, algorithms="HS256")

    except jwt.exceptions.ExpiredSignatureError as e:
        raise HTTPException(UNAUTHORIZED, f"Token expirado, msg: {e}")

    # except jwt.exceptions.InvalidTokenError as e:
    #     raise HTTPException(BAD_REQUEST, f"Token inválido, msg: {e}")

    # except jwt.DecodeError as e:
    #     raise HTTPException(
    #         INTERNAL_SERVER_ERROR, f"Erro desconhecido validando token, msg: {e}"
    # )
    else:
        return int(decoded["sub"])

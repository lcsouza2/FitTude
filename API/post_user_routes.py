from asyncio import create_task
from uuid import uuid4, UUID

import argon2
import Database.db_mapping as tables
import schemas
from argon2 import PasswordHasher
from Database.utils import (
    AsyncSession,
    redis_pool,
    generate_refresh_token,
    generate_session_token,
)
from Email.email_verify import send_verification_mail
from fastapi import FastAPI, HTTPException, Request
from pydantic import validate_email
from pydantic_core import PydanticCustomError
from sqlalchemy import exc, insert, or_, select

hasher = PasswordHasher()
POST_APP = FastAPI(title="Main API POST Routes")


@POST_APP.post("/register")
async def begin_register(user: schemas.User):
    """Envia um email de confirmação do cadastro para o email fornecido,
    depois armazena os dados fornecidos em um cache para validar o cadastro"""

    try:
        validate_email(user.email)
    except PydanticCustomError:
        raise HTTPException(422, "Email Inválido")

    # Envia o email assíncronamente
    request_protocol = uuid4()
    await create_task(
        send_verification_mail(
            user.email, protocol=request_protocol, username=user.username
        )
    )

    # Armazena os dados do usuário em cache
    with redis_pool() as cache_storage:
        cache_storage.hset(f"protocol:{request_protocol}", mapping=user.model_dump())


@POST_APP.get("/register/confirm/{protocol}")
async def create_register(protocol: UUID):
    """Efetiva o registro no banco
       recebendo uma requisição referente ao protocolo gerado"""

    # Obtem os dados do usuário no cache
    with redis_pool() as cache_storage:
        user_data = cache_storage.hgetall(f"protocol:{protocol}")

        if not user_data:
            raise HTTPException(
                404, "Não existem dados referentes a esse protocolo, tente novamente"
            )

        user_data["password"] = hasher.hash(user_data.get("password"))

    # Tenta criar o usuário no banco
    async with AsyncSession() as session:
        try:
            await session.execute(insert(tables.Usuario).values(user_data))
            await session.commit()
        # Tratamento para duplicidade
        except exc.IntegrityError as e:
            if "uq_usuario_username" in str(e):
                raise HTTPException(
                    409, "Esse nome de usuário já está sendo usado!"
                )
            if "uq_usuario_email" in str(e):
                raise HTTPException(409, "Esse email já está sendo usado!")
        else:
            cache_storage.delete(f"protocol:{protocol}")
            return {generate_session_token(id_or_email=user_data.get("email"))}


@POST_APP.post("/login")
async def login_user(user: schemas.UserLogin):
    """Procura o usuário no banco e valida a senha,
       se válida retorna 2 tokens, senão, levanta erro"""

    async with AsyncSession() as a_ssession:
        # Busca o usuário no banco
        result = await a_ssession.execute(
            select(tables.Usuario).where(
                or_(
                    tables.Usuario.username == user.username,
                    tables.Usuario.email == user.email,
                )
            )
        )

    found = result.scalars().first()

    # Verifica se existe
    if not found:
        raise HTTPException(404, "Usuário não encontrado")

    # Verifica a senha se o usuário existir
    if not argon2.verify_password(found.password, user.password):
        raise HTTPException(409, "Senha incorreta")

    # Se não houverem erros retorna os tokens

    if not user.keep_login:
        return {
            "session_token": generate_session_token(
                found.id_usuario, expire_in_a_day=True
            )
        }

    return {
        "refresh_token": generate_refresh_token(found.id_usuario),
        "session_token": generate_session_token(found.id_usuario),
    }

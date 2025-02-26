from http.client import (
    BAD_REQUEST,
    CONFLICT,
    INTERNAL_SERVER_ERROR,
    NOT_FOUND,
    UNAUTHORIZED,
    UNPROCESSABLE_ENTITY,
)
from uuid import UUID, uuid4

import Database.db_mapping as tables
import jwt
import schemas
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from Database.utils import (
    JWT_REFRESH_KEY,
    AsyncSession,
    generate_refresh_token,
    generate_register_token,
    generate_session_token,
    redis_pool,
)
from Email.email_verify import send_verification_mail
from fastapi import BackgroundTasks, FastAPI, HTTPException
from pydantic import validate_email
from pydantic_core import PydanticCustomError
from sqlalchemy import exc, insert, or_, select

hasher = PasswordHasher()

USER_API_POST = FastAPI(title="Rotas POST para serivços de usuários")

@USER_API_POST.post("/register")  # Rota para começar o registro do usuário.
async def begin_register(user: schemas.UserRegister, bg_tasks: BackgroundTasks):
    """Envia um email de confirmação do cadastro para o email fornecido,
    depois armazena os dados fornecidos no redis para validar o cadastro"""

    try:
        validate_email(
            user.email
        )  # Começa validando o email, ser for inválido já encerra a função.
    except PydanticCustomError:
        raise HTTPException(UNPROCESSABLE_ENTITY, "Email Inválido")

    # Envia o email assíncronamente
    request_protocol = uuid4()
    bg_tasks.add_task(
        send_verification_mail, user.email, protocol=request_protocol, username=user.username
    )

    # Armazena os dados do usuário
    with redis_pool() as cache_storage:
        cache_storage.hset(f"protocol:{request_protocol}", mapping=user.model_dump())
        cache_storage.expire(
            f"protocol:{request_protocol}", 1800
        )  # 1800 segundos == 30 min


@USER_API_POST.get("/register/confirm/{protocol}")
async def create_register(protocol: UUID):
    """Efetiva o registro no banco
    recebendo uma requisição referente ao protocolo gerado"""

    # Obtem os dados do usuário no redis
    with redis_pool() as cache_storage:
        user_data = cache_storage.hgetall(f"protocol:{protocol}")

        if not user_data:
            raise HTTPException(
                NOT_FOUND, "Protocolo inválido, já finalizado, ou expirado"
            )

        user_data["password"] = hasher.hash(user_data.get("password"))

    # Tenta criar o usuário no banco
    async with AsyncSession() as session:
        try:
            await session.execute(insert(tables.Usuario).values(user_data))

        # Tratamento para duplicidade
        except exc.IntegrityError as e:
            if "uq_usuario_username" in str(e):
                raise HTTPException(
                    CONFLICT, "Esse nome de usuário já está sendo usado!"
                )
            if "uq_usuario_email" in str(e):
                raise HTTPException(CONFLICT, "Esse email já está sendo usado!")
        else:
            try:
                token = generate_register_token(email=user_data.get("email"))
            except jwt.exceptions.PyJWTError:
                raise HTTPException(
                    INTERNAL_SERVER_ERROR, "Erro desconhecido gerando token"
                )
            else:
                await session.flush()
                await session.commit()
                redis_pool().delete(f"protocol:{protocol}")
                return {"token": token}


@USER_API_POST.post("/login")
async def login_user(user: schemas.UserLogin):
    """Procura o usuário no banco e valida a senha,
    se válida retorna 2 tokens, senão, levanta erro"""

    async with AsyncSession() as session:
        # Busca o usuário no banco
        result = await session.execute(
            select(tables.Usuario).where(
                or_(
                    tables.Usuario.username == user.login_key,
                    tables.Usuario.email == user.login_key,
                )
            )
        )

        found = result.scalars().first()

    # Verifica se existe
    if found is None:
        raise HTTPException(NOT_FOUND, "Usuário não encontrado")

    # Verifica a senha se o usuário existir
    try:
        hasher.verify(found.password, user.password)
    except VerifyMismatchError:
        raise HTTPException(NOT_FOUND, "Senha incorreta")

    # Se não houverem erros retorna os tokens
    try:
        if not user.keep_login:
            token = await generate_session_token(found.id_usuario)

            return {"session_token": token}

        ref_token = await generate_refresh_token(found.id_usuario)
        ses_token = await generate_session_token(found.id_usuario)

        return {
            "refresh_token": ref_token,
            "session_token": ses_token,
        }

    except jwt.exceptions.PyJWTError as e:
        raise HTTPException(
            INTERNAL_SERVER_ERROR, f"Erro desconhecido gerando token, {e}"
        )


@USER_API_POST.post(
    "/renew_token"
)  # Rota para requisitar um novo token de sessão caso expire
async def renew_token(token: schemas.TokenRenew) -> str:
    """
    Decodifica o token de sessão do usuário e tenta gerar um token de sessão com ele
    Returns:
        token em formato str
    """

    # Tenta decodificar o token
    try:
        decoded = jwt.decode(token.refresh_token, JWT_REFRESH_KEY, algorithms=["HS256"])

        # Se o reresh token estiver expirado ele levanta erro 401()
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(UNAUTHORIZED, "Token de renovação expirado")

        # Se o token extiver inválido (alterado no cliente) levanda o erro 400
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(BAD_REQUEST, f"Token inválido recebido, msg {e}")

        # Se não ocorrerem errosretorna um novo token de sessão
    else:
        return await generate_refresh_token(decoded["sub"])

from fastapi import FastAPI, Request
import schemas
from Email.email_verify import send_verification_mail
from asyncio import create_task
from uuid import uuid4
from Database.db_utils import RedisPoll, AsyncSession
from sqlalchemy import insert
import Database.db_mapping as tables


POST_APP = FastAPI(title="Main API POST Routes")

@POST_APP.post("/register")
async def begin_register(user: schemas.User):
    """Envia um email de confirmação do cadastro para o email fornecido,
    depois armazena os dados fornecidos em um cache para validar o cadastro"""

    # Envia o email assíncronamente
    request_protocol=uuid4()
    await create_task(send_verification_mail(user.email, protocol=request_protocol, username=user.username))

    # Armazena os dados do usuário em cache
    with RedisPoll() as cache_storage:
        cache_storage.hset(f"protocol:{request_protocol}", mapping=user.model_dump())



@POST_APP.post("/register/confirm/{protocol}")
async def create_register(request: Request, protocol):

    with RedisPoll() as cache_storage:
        user_data = cache_storage.hgetall(f"protocol:{protocol}")

    async with AsyncSession() as session:
        await session.execute(insert(tables.Usuario).values(user_data))
        await session.commit()
        

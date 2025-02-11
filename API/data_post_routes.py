import Database.db_mapping as tables
import schemas
from Database.utils import AsyncSession, validate_token
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from user_routes import POST_APP

DATA_POST_API = FastAPI(title="Requisitar criação de dados")

DATA_POST_API.mount("/user", POST_APP, "Rotas de gerenciamento de usuários")

@DATA_POST_API.post("/equipment/new")
async def criar_novo_aparelho(
    aparelho: schemas.Aparelho, id_usuario: int = Depends(validate_token)
):
    async with AsyncSession() as session:
        try:
            await session.scalars(
                insert(tables.Aparelho).values(
                    {**aparelho.model_dump(), "id_usuario": id_usuario}
                )
            )
            await session.commit()
        except IntegrityError as e:
            if "uq_aparelho" in str(e):
                raise HTTPException(409, "Esse aparelho já existe")


@DATA_POST_API.post("/muscle/new")
async def criar_novo_musculo(
    musculo: schemas.Musculo, id_usuario: int = Depends(validate_token)
):
    async with AsyncSession() as session:
        try:
            await session.scalars(
                insert(tables.Musculo).values(
                    {**musculo.model_dump(), "id_usuario": id_usuario}
                )
            )
            await session.commit()
        except IntegrityError as e:
            if "uq_musculo" in str(e):
                raise HTTPException(409, "Esse musculo já existe")


@DATA_POST_API.post("/exercise/new")
async def criar_novo_exercicio(
    exercicio: schemas.Exercicio, id_usuario: int = Depends(validate_token)
):
    async with AsyncSession() as session:
        try:
            await session.scalars(
                insert(tables.Exercicio).values(
                    {**exercicio.model_dump(), "id_usuario": id_usuario}
                )
            )
            await session.commit()
        except IntegrityError as e:
            if "uq_exercicio" in str(e):
                raise HTTPException(409, "Esse exercicio já existe")
            

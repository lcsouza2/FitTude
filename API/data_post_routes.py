from http.client import CONFLICT
from typing import List

import Database.db_mapping as tables
import schemas
from Database.utils import AsyncSession, validate_token
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from user_routes import POST_APP

DATA_POST_API = FastAPI(title="Requisitar criação de dados")

# Monta a aplicação de gerenciamentos de usuário nessa apolicação, usando a rota /user/
DATA_POST_API.mount("/user", POST_APP, "Rotas de gerenciamento de usuários")


@DATA_POST_API.post("/equipment/new")
async def criar_novo_aparelho(
    aparelho: schemas.Aparelho,
    id_usuario: int = Depends(validate_token),  # Valida o token JWT
):
    """
    Tenta criar o aparelho enviado pelo usuário no banco de dados
    """

    async with AsyncSession() as session:
        try:
            # Executa o insert
            await session.scalars(
                insert(tables.Aparelho).values(
                    # Desempacota o aparelho num dicionário e acrescenta o id_usuário
                    {**aparelho.model_dump(), "id_usuario": id_usuario}
                )
            )
            await session.commit()

        # Tratamento para duplicidade
        except IntegrityError as e:
            if "uq_aparelho" in str(e):
                raise HTTPException(CONFLICT, "Esse aparelho já existe")


@DATA_POST_API.post("/muscle/new")
async def criar_novo_musculo(
    musculo: schemas.Musculo, id_usuario: int = Depends(validate_token)
):
    """Adiciona um novo músculo personalizado pelo usuário ao banco de dados"""

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
                raise HTTPException(CONFLICT, "Esse musculo já existe")


@DATA_POST_API.post("/exercise/new")
async def criar_novo_exercicio(
    exercicio: schemas.Exercicio, id_usuario: int = Depends(validate_token)
):
    """Adiciona um exercício personalizado pelo usuário ao banco de dados"""

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
                raise HTTPException(CONFLICT, "Esse exercicio já existe")


@DATA_POST_API.post("/workout/sheet/new")


async def criar_nova_ficha_treino(
    ficha_treino: schemas.FichaTreino, id_usuario: int = Depends(validate_token)
):
    """Cria uma nova ficha de treino"""

    async with AsyncSession() as session:
        try:
            await session.scalars(
                insert(tables.FichaTreino).values(
                    {**ficha_treino.model_dump(), "id_usuario": id_usuario}
                )
            )
            await session.commit()
        except IntegrityError as e:
            if "uq_ficha_treino" in str(e):
                raise HTTPException(CONFLICT, "Essa ficha de treino já existe")


@DATA_POST_API.post("/workout/division/new")


async def criar_nova_divisao_treino(divisao: schemas.DivisaoTreino):
    """Adiciona uma nova divisão de treino a uma ficha de treino"""

    validate_token()

    async with AsyncSession() as session:
        try:
            await session.scalars(
                insert(tables.DivisaoTreino).values(divisao.model_dump())
            )
            await session.commit()
        except IntegrityError as e:
            if "pk_divisao_treino" in str(e):
                raise HTTPException(CONFLICT, "Essa divisao de treino já existe")


@DATA_POST_API.post("/workout/division/add_exercise")


async def adicionar_exercicio_divisao(exercicios: List[schemas.DivisaoExercicio]):
    """Adiciona uma lista de exercícios a uma divisão de treino"""

    validate_token()

    async with AsyncSession() as session:
        try:
            for i in exercicios:
                await session.scalars(
                    insert(tables.DivisaoExercicio).values(i.model_dump())
                )
            await session.commit()
        except IntegrityError as e:
            if "pk_divisao_exercicio" in str(e):
                raise HTTPException(
                    CONFLICT, "Esse exercicio já foi adicionado a essa divisão"
                )


@DATA_POST_API.post("/workout/report/new_report")


async def criar_novo_relatorio(relatorio: schemas.RelatorioTreino):
    """Cria um relatório de treino"""

    validate_token()

    async with AsyncSession() as session:
        try:
            await session.scalars(
                insert(tables.DivisaoExercicio).values(relatorio.model_dump())
            )
            await session.commit()
        except IntegrityError as e:
            if "pk_relatorio_treino" in str(e):
                raise HTTPException(CONFLICT, "Esse relatório já existe")


@DATA_POST_API.post("/workout/report/add_exercise")
async def adicionar_exercicio_relatorio(exercicios: List[schemas.SerieRelatorio]):
    """Adiciona uma lista de exercícios feitos a um relatório de treino"""

    validate_token()

    async with AsyncSession() as session:
        try:
            for i in exercicios:
                await session.scalars(
                    insert(tables.SerieRelatorio).values(i.model_dump())
                )
                await session.commit()
        except IntegrityError as e:
            if "pk_series_relatorio" in str(e):
                raise HTTPException(
                    CONFLICT, "Essa série já foi adicionada a esse relatório"
                )
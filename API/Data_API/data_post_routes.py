from http.client import CONFLICT
from typing import List

import Database.db_mapping as tables
from Database import schemas
from Database.utils import (
    AsyncSession,
    validate_token,
)
from fastapi import FastAPI, HTTPException, Request, Response
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from Database import utils

DATA_API = FastAPI(title="Rotas POST para serviços de treinos")


@DATA_API.post("/equipment/new")
async def criar_novo_aparelho(
    aparelho: schemas.Aparelho, request: Request, response: Response
):
    """
    Tenta criar o aparelho enviado pelo usuário no banco de dados
    """

    id_usuario = await validate_token(request, response)

    async with AsyncSession() as session:
        try:
            # Executa o insert
            await session.execute(
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


@DATA_API.post("/muscle/new")
async def criar_novo_musculo(
    musculo: schemas.Musculo, request: Request, response: Response
):
    """Adiciona um novo músculo personalizado pelo usuário ao banco de dados"""

    id_usuario = await validate_token(request, response)

    async with AsyncSession() as session:
        try:
            await session.execute(
                insert(tables.Musculo).values(
                    {**musculo.model_dump(), "id_usuario": id_usuario}
                )
            )
            await session.commit()
        except IntegrityError as e:
            if "uq_musculo" in str(e):
                raise HTTPException(CONFLICT, "Esse musculo já existe")


@DATA_API.post("/exercise/new")
async def criar_novo_exercicio(
    exercicio: schemas.Exercicio, request: Request, response: Response
):
    """Adiciona um exercício personalizado pelo usuário ao banco de dados"""

    id_usuario = await validate_token(request, response)

    async with AsyncSession() as session:
        try:
            await session.execute(
                insert(tables.Exercicio).values(
                    {**exercicio.model_dump(), "id_usuario": id_usuario}
                )
            )
            await session.commit()
        except IntegrityError as e:
            if "uq_exercicio" in str(e):
                raise HTTPException(CONFLICT, "Esse exercicio já existe")


@DATA_API.post("/workout/sheet/new")
async def criar_nova_ficha_treino(
    ficha_treino: schemas.FichaTreino, request: Request, response: Response
):
    """Cria uma nova ficha de treino"""

    id_usuario = await validate_token(request, response)

    async with AsyncSession() as session:
        try:
            await session.execute(
                insert(tables.FichaTreino).values(
                    {**ficha_treino.model_dump(), "id_usuario": id_usuario}
                )
            )
            await session.commit()
        except IntegrityError as e:
            if "uq_ficha_treino" in str(e):
                raise HTTPException(CONFLICT, "Essa ficha de treino já existe")


@DATA_API.post("/workout/division/new")
async def criar_nova_divisao_treino(
    divisao: schemas.DivisaoTreino, request: Request, response: Response
):
    """Adiciona uma nova divisão de treino a uma ficha de treino"""

    await validate_token(request, response)

    async with AsyncSession() as session:
        try:
            await session.execute(
                insert(tables.DivisaoTreino).values(divisao.model_dump())
            )
            await session.commit()
        except IntegrityError as e:
            if "pk_divisao_treino" in str(e):
                raise HTTPException(CONFLICT, "Essa divisao de treino já existe")


@DATA_API.post("/workout/division/add_exercise")
async def adicionar_exercicio_divisao(
    exercicios: List[schemas.DivisaoExercicio], request: Request, response: Response
):
    """Adiciona uma lista de exercícios a uma divisão de treino"""

    await validate_token(request, response)

    async with AsyncSession() as session:
        # try:
        valores = [i.model_dump() for i in exercicios]
        await session.execute(insert(tables.DivisaoExercicio).values(valores))
        await session.commit()
    # except IntegrityError as e:
    #     if "pk_divisao_exercicio" in str(e):
    #         raise HTTPException(
    #             CONFLICT, "Esse exercicio já foi adicionado a essa divisão"
    # )


@DATA_API.post("/workout/report/new_report")
async def criar_novo_relatorio(
    relatorio: schemas.RelatorioTreino, request: Request, response: Response
):
    """Cria um relatório de treino"""

    await validate_token(request, response)

    async with AsyncSession() as session:
        try:
            await session.execute(
                insert(tables.DivisaoExercicio).values(relatorio.model_dump())
            )
            await session.commit()
        except IntegrityError as e:
            if "pk_relatorio_treino" in str(e):
                raise HTTPException(CONFLICT, "Esse relatório já existe")


@DATA_API.post("/workout/report/add_exercise")
async def adicionar_exercicio_relatorio(
    exercicios: List[schemas.SerieRelatorio], request: Request, response: Response
):
    """Adiciona uma lista de exercícios feitos a um relatório de treino"""

    await validate_token(request, response)

    async with AsyncSession() as session:
        try:
            for i in exercicios:
                await session.execute(
                    insert(tables.SerieRelatorio).values(i.model_dump())
                )
                await session.commit()
        except IntegrityError as e:
            if "pk_series_relatorio" in str(e):
                raise HTTPException(
                    CONFLICT, "Essa série já foi adicionada a esse relatório"
                )

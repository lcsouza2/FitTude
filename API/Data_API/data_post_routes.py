from http.client import CONFLICT, NOT_FOUND
from typing import List

import Database.db_mapping as tables
from Data_API.data_get_routes import DATA_API
from Database import schemas
from Database.utils import (
    AsyncSession,
    validate_token,
)
from fastapi import Depends, HTTPException
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError


@DATA_API.post("/equipment/new")
async def create_new_equipment(
    equipment: schemas.Aparelho, user_id: int = Depends(validate_token)
):
    """
    Tenta criar o aparelho enviado pelo usuário no banco de dados
    """

    async with AsyncSession() as session:
        try:
            await session.execute(
                insert(tables.Aparelho).values(
                    {**equipment.model_dump(), "id_usuario": user_id}
                )
            )
            await session.commit()

        except IntegrityError as e:
            if "uq_aparelho" in str(e):
                raise HTTPException(CONFLICT, "Esse aparelho já existe")


@DATA_API.post("/muscle/new")
async def create_new_muscle(
    muscle: schemas.Musculo, user_id: int = Depends(validate_token)
):
    """Adiciona um novo músculo personalizado pelo usuário ao banco de dados"""

    async with AsyncSession() as session:
        try:
            await session.execute(
                insert(tables.Musculo).values(
                    {**muscle.model_dump(), "id_usuario": user_id}
                )
            )
            await session.commit()
        except IntegrityError as e:
            if "uq_musculo" in str(e):
                raise HTTPException(CONFLICT, "Esse musculo já existe")


@DATA_API.post("/exercise/new")
async def create_new_exercise(
    exercise: schemas.Exercicio, user_id: int = Depends(validate_token)
):
    """Adiciona um exercício personalizado pelo usuário ao banco de dados"""

    async with AsyncSession() as session:
        try:
            await session.execute(
                insert(tables.Exercicio).values(
                    {**exercise.model_dump(), "id_usuario": user_id}
                )
            )
            await session.commit()
        except IntegrityError as e:
            if "uq_exercicio" in str(e):
                raise HTTPException(CONFLICT, "Esse exercicio já existe")


@DATA_API.post("/workout/sheet/new")
async def create_new_workout_sheet(
    sheet: schemas.FichaTreino, user_id: int = Depends(validate_token)
):
    """Cria uma nova ficha de treino"""

    async with AsyncSession() as session:
        try:
            await session.execute(
                insert(tables.FichaTreino).values(
                    {**sheet.model_dump(), "id_usuario": user_id}
                )
            )
            await session.commit()
        except IntegrityError as e:
            if "uq_ficha_treino" in str(e):
                raise HTTPException(CONFLICT, "Essa ficha de treino já existe")


@DATA_API.post("/workout/division/new")
async def criar_nova_divisao_treino(
    division: schemas.DivisaoTreino, user_id: int = Depends(validate_token)
):
    """Adiciona uma nova divisão de treino a uma ficha de treino"""

    async with AsyncSession() as session:
        try:
            await session.execute(
                insert(tables.DivisaoTreino).values(division.model_dump())
            )
            await session.commit()
        except IntegrityError as e:
            if "pk_divisao_treino" in str(e):
                raise HTTPException(CONFLICT, "Essa divisao de treino já existe")


@DATA_API.post("/workout/division/add_exercise")
async def add_exercise_to_division(
    exercises: List[schemas.DivisaoExercicio], user_id: int = Depends(validate_token)
):
    """Adiciona uma lista de exercícios a uma divisão de treino"""

    async with AsyncSession() as session:
        try:
            valores = [i.model_dump() for i in exercises]
            await session.execute(insert(tables.DivisaoExercicio).values(valores))
            await session.commit()

        except IntegrityError as exc:
            if "pk_divisao_exercicio" in str(exc):
                raise HTTPException(
                    CONFLICT, "Esse exercicio já foi adicionado a essa divisão"
                )

            if "fk_divisao_exercicio_divisao_treino" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "A divisão de treino referenciada não existe"
                )

            if "fk_divisao_exercicio_exercicio" in str(exc):
                raise HTTPException(NOT_FOUND, "O exercício referenciado não existe")


@DATA_API.post("/workout/report/new_report")
async def create_new_report(
    report: schemas.RelatorioTreino, user_id: int = Depends(validate_token)
):
    """Cria um relatório de treino"""

    async with AsyncSession() as session:
        try:
            await session.execute(
                insert(tables.DivisaoExercicio).values(report.model_dump())
            )
            await session.commit()

        except IntegrityError as exc:
            if "pk_relatorio_treino" in str(exc):
                raise HTTPException(CONFLICT, "Esse relatório já existe")

            if "fk_relatorio_treino_divisao_treino" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "A divisão de treino referenciada não existe"
                )


@DATA_API.post("/workout/report/add_exercise")
async def add_exercise_to_report(
    exercises: List[schemas.SerieRelatorio], user_id: int = Depends(validate_token)
):
    """Adiciona uma lista de exercícios feitos a um relatório de treino"""

    async with AsyncSession() as session:
        try:
            for i in exercises:
                await session.execute(
                    insert(tables.SerieRelatorio).values(i.model_dump())
                )
                await session.commit()
        except IntegrityError as exc:
            if "pk_series_relatorio" in str(exc):
                raise HTTPException(
                    CONFLICT, "Essa série já foi adicionada a esse relatório"
                )

            if "fk_serie_relatorio_divisao_exercicio" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "O exercício referenciado não existe na divisão"
                )

            if "fk_serie_relatorio_relatorio_treino" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "O relatório de treino referenciado não existe"
                )

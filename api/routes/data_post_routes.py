from typing import List, Any, Dict, Optional
from sqlalchemy.orm import MappedAsDataclass, InstrumentedAttribute
from fastapi import Depends, HTTPException, APIRouter
from http import HTTPStatus
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from core.exceptions import PrimaryKeyViolation, ForeignKeyViolation, UniqueConstraintViolation, EntityNotFound
from core.connections import AsyncSession
from core.authetication import TokenService

from database import db_mapping
from core import schemas

DATA_POST_API = APIRouter(prefix="/api/data")


async def _execute_insert(
    *,
    table: MappedAsDataclass,
    values: Dict[str, Any],
    error_mapping: List[schemas.ConstraintErrorHandling],
    entity_name: str,
) -> str:
    """
    Executa uma operação de inserção genérica no banco de dados.

    Args:
        table: Classe do modelo SQLAlchemy a ser inserido
        values: Dicionário com os valores a serem inseridos
        error_mapping: Lista de dicionários com mapeamento de erros
        entity_name: Nome da entidade para mensagens de erro

    Returns:
        str: Mensagem de sucesso

    Raises:
        HTTPException: Para violações de constraint do banco
    """
    async with AsyncSession() as session:
        try:
            await session.execute(insert(table).values(values))
            await session.commit()
            return f"{entity_name} criado com sucesso"

        except IntegrityError as exc:
            await session.rollback()
            for error in error_mapping:
                if error.get("constraint") in str(exc):
                    raise error.get("error")(error.get("message"))
            # Se não encontrou erro mapeado, re-raise a exceção original
            raise


@DATA_POST_API.post("/equipment/new")
async def create_new_equipment(
    equipment: schemas.Aparelho, user_id: int = Depends(TokenService.validate_token)
):
    """
    Tenta criar o aparelho enviado pelo usuário no banco de dados
    """
    return await _execute_insert(
        table=db_mapping.Aparelho,
        values={**equipment.model_dump(), "id_usuario": user_id},
        error_mapping=[
            {
                "constraint": "uq_aparelho", 
                "message": "Esse aparelho já existe"
            }
        ],
        entity_name="Aparelho",
    )


@DATA_POST_API.post("/muscle/new")
async def create_new_muscle(
    muscle: schemas.Musculo, user_id: int = Depends(TokenService.validate_token)
):
    """Adiciona um novo músculo personalizado pelo usuário ao banco de dados"""
    return await _execute_insert(
        table=db_mapping.Musculo,
        values={**muscle.model_dump(), "id_usuario": user_id},
        error_mapping=[
            {"constraint": "uq_musculo", "message": "Esse musculo já existe"}
        ],
        entity_name="Musculo",
    )


@DATA_POST_API.post("/exercise/new")
async def create_new_exercise(
    exercise: schemas.Exercicio, user_id: int = Depends(TokenService.validate_token)
):
    """Adiciona um exercício personalizado pelo usuário ao banco de dados"""
    return await _execute_insert(
        table=db_mapping.Exercicio,
        values={**exercise.model_dump(), "id_usuario": user_id},
        error_mapping=[
            {"constraint": "uq_exercicio", "message": "Esse exercicio já existe"}
        ],
        entity_name="Exercicio",
    )


@DATA_POST_API.post("/workout/sheet/new")
async def create_new_workout_sheet(
    sheet: schemas.FichaTreino, user_id: int = Depends(TokenService.validate_token)
):
    """Cria uma nova ficha de treino"""
    return await _execute_insert(
        table=db_mapping.FichaTreino,
        values={**sheet.model_dump(), "id_usuario": user_id},
        error_mapping=[
            {"constraint": "uq_ficha_treino", "message": "Essa ficha de treino já existe"}
        ],
        entity_name="FichaTreino",
    )


@DATA_POST_API.post("/workout/division/new")
async def criar_nova_divisao_treino(
    division: schemas.DivisaoTreino, user_id: int = Depends(TokenService.validate_token)
):
    """Adiciona uma nova divisão de treino a uma ficha de treino"""
    return await _execute_insert(
        table=db_mapping.DivisaoTreino,
        values=division.model_dump(),
        error_mapping=[
            {"constraint": "pk_divisao_treino", "message": "Essa divisao de treino já existe"}
        ],
        entity_name="DivisaoTreino",
    )


@DATA_POST_API.post("/workout/division/add_exercise")
async def add_exercise_to_division(
    exercises: List[schemas.DivisaoExercicio], user_id: int = Depends(TokenService.validate_token)
):
    """Adiciona uma lista de exercícios a uma divisão de treino"""

    async with AsyncSession() as session:
        try:
            valores = [i.model_dump() for i in exercises]
            await session.execute(insert(db_mapping.DivisaoExercicio).values(valores))
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


@DATA_POST_API.post("/workout/report/new_report")
async def create_new_report(
    report: schemas.RelatorioTreino, user_id: int = Depends(TokenService.validate_token)
):
    """Cria um relatório de treino"""
    return await _execute_insert(
        table=db_mapping.RelatorioTreino,
        values=report.model_dump(),
        error_mapping=[
            {"constraint": "pk_relatorio_treino", "message": "Esse relatório já existe"},
            {"constraint": "fk_relatorio_treino_divisao_treino", "message": "A divisão de treino referenciada não existe", "status": HTTPStatus.NOT_FOUND}
        ],
        entity_name="RelatorioTreino",
    )


@DATA_POST_API.post("/workout/report/add_exercise")
async def add_exercise_to_report(
    exercises: List[schemas.SerieRelatorio], user_id: int = Depends(TokenService.validate_token)
):
    """Adiciona uma lista de exercícios feitos a um relatório de treino"""

    async with AsyncSession() as session:
        # try:
        for i in exercises:
            await session.execute(insert(db_mapping.SerieRelatorio).values(i.model_dump()))
            await session.commit()
    # except IntegrityError as exc:
    #     if "pk_series_relatorio" in str(exc):
    #         raise HTTPException(
    #             CONFLICT, "Essa série já foi adicionada a esse relatório"
    #         )

    #     if "fk_serie_relatorio_divisao_exercicio" in str(exc):
    #         raise HTTPException(
    #             NOT_FOUND, "O exercício referenciado não existe na divisão"
    #         )

    #     if "fk_serie_relatorio_relatorio_treino" in str(exc):
    #         raise HTTPException(
    #             NOT_FOUND, "O relatório de treino referenciado não existe"
    #         )

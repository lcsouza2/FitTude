from http.client import CONFLICT, NOT_FOUND
from typing import Any, Dict, List, Optional

from ..database import db_mapping
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import and_, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute, MappedAsDataclass
from sqlalchemy.sql.expression import BinaryExpression

from core import schemas
from core.authetication import TokenService
from core.connections import db_connection
from core.exceptions import (
    EntityNotFound,
    ForeignKeyViolation,
    UniqueConstraintViolation,
)
from core.utils import exclude_falsy_from_dict

DATA_PUT_API = APIRouter(prefix="/api/data")


async def _execute_update(
    *,
    table: MappedAsDataclass,
    entity_name: str,
    where_clause: BinaryExpression,
    values_mapping: Dict[InstrumentedAttribute, Any],
    session: AsyncSession,
    error_mapping: List[schemas.ConstraintErrorHandling],
    returning_column: Optional[InstrumentedAttribute],
):
    async with session:
        try:
            result = await session.execute(
                update(table)
                .where(where_clause)
                .values(exclude_falsy_from_dict(values_mapping))
                .returning(returning_column)
            )
        except IntegrityError as exc:
            await session.rollback()
            for error in error_mapping:
                if error.get("constraint") in str(exc):
                    raise error.get("error")(error.get("message"))
        else:
            if result.scalar_one_or_none() is None:
                await session.rollback()
                raise EntityNotFound(f"{entity_name} não encontrado(a)")

            await session.commit()
            return "Alterado"


@DATA_PUT_API.put("/muscle/update/{muscle_id}")
async def update_muscle(
    muscle_id: int,
    updates: schemas.MusculoAlterar,
    user_id: int = Depends(TokenService.validate_token),
    session: AsyncSession = Depends(db_connection),
):

    await _execute_update(
        table=db_mapping.Musculo,
        entity_name="Músculo",
        where_clause=and_(
            db_mapping.Musculo.id_musculo == muscle_id,
            db_mapping.Musculo.id_usuario == user_id,
        ),
        values_mapping=updates.model_dump(exclude_none=True),
        session=session,
        error_mapping=[
            {
                "constraint": "uq_musculo",
                "error": UniqueConstraintViolation,
                "message": "Os dados recebidos conflitam com algum registro existente!",
            },
            {
                "constraint": "fk_musculo_grupamento",
                "error": ForeignKeyViolation,
                "message": "O grupamento referenciado não foi encontrado",
            },
            {
                "constraint": "fk_musculo_usuario",
                "error": ForeignKeyViolation,
                "message": "O usuário referenciado não foi encontrado",
            },
        ],
        returning_column=db_mapping.Musculo.id_musculo,
    )



@DATA_PUT_API.put("/equipment/update/{equipment_id}")
async def update_equipment(
    equipment_id: int,
    updates: schemas.AparelhoAlterar,
    user_id: int = Depends(TokenService.validate_token),
):
    async with AsyncSession() as session:
        try:
            result = await session.execute(
                update(db_mapping.Aparelho)
                .where(
                    and_(
                        db_mapping.Aparelho.id_aparelho == equipment_id,
                        db_mapping.Aparelho.id_usuario == user_id,
                    )
                )
                .values(exclude_falsy_from_dict(updates.model_dump(exclude_none=True)))
                .returning(db_mapping.Aparelho.id_aparelho)
            )
        except IntegrityError as exc:
            await session.rollback()
            if "uq_aparelho" in str(exc):
                raise HTTPException(
                    CONFLICT,
                    "Os dados recebidos conflitam com algum registro existente!",
                )
            elif "fk_aparelho_grupamento" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "O grupamento referenciado não foi encontrado"
                )
        else:
            if result.scalar_one_or_none() is None:
                await session.rollback()
                raise HTTPException(NOT_FOUND, "Aparelho não encontrado")
            await session.commit()


@DATA_PUT_API.put("/exercise/update/{exercise_id}")
async def update_exercise(
    exercise_id: int,
    updates: schemas.ExercicioAlterar,
    user_id: int = Depends(TokenService.validate_token),
):
    async with AsyncSession() as session:
        try:
            result = await session.execute(
                update(db_mapping.Exercicio)
                .where(
                    and_(
                        db_mapping.Exercicio.id_exercicio == exercise_id,
                        db_mapping.Exercicio.id_usuario == user_id,
                    )
                )
                .values(exclude_falsy_from_dict(updates.model_dump(exclude_none=True)))
                .returning(db_mapping.Exercicio.id_exercicio)
            )
        except IntegrityError as exc:
            await session.rollback()
            if "uq_exercicio" in str(exc):
                raise HTTPException(
                    CONFLICT,
                    "Os dados recebidos conflitam com algum registro existente!",
                )
            elif "fk_exercicio_aparelho" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "O aparelho referenciado não foi encontrado "
                )
            elif "fk_exercicio_musculo" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "O músculo referenciado não foi encontrado "
                )

        else:
            if result.scalar_one_or_none() is None:
                await session.rollback()
                raise HTTPException(NOT_FOUND, "Exercício não econtrado")
            await session.commit()


@DATA_PUT_API.put("/workout/sheet/update/{sheet_id}")
async def update_workout_sheet(
    sheet_id: int,
    updates: schemas.FichaTreinoAlterar,
    user_id: int = Depends(TokenService.validate_token),
):
    async with AsyncSession() as session:
        try:
            result = await session.execute(
                update(db_mapping.FichaTreino)
                .where(
                    and_(
                        db_mapping.FichaTreino.id_ficha_treino == sheet_id,
                        db_mapping.FichaTreino.id_usuario == user_id,
                    )
                )
                .values(exclude_falsy_from_dict(updates.model_dump(exclude_none=True)))
                .returning(db_mapping.FichaTreino.id_ficha_treino)
            )
        except IntegrityError as exc:
            await session.rollback()
            if "uq_ficha_treino" in str(exc):
                raise HTTPException(
                    CONFLICT,
                    "O nome da recebido já é usado por outra ficha de treino",
                )
        else:
            if result.scalar_one_or_none() is None:
                raise HTTPException(NOT_FOUND, "Ficha de treino não encontrada")
            await session.commit()


@DATA_PUT_API.put("/workout/division/update/{division}")
async def update_workout_division(
    division: str,
    new_division_name: str = Query(
        max_length=20, description="Novo nome da divisão especificada"
    ),
    user_id: int = Depends(TokenService.validate_token),
):
    async with AsyncSession() as session:
        try:
            result = await session.execute(
                update(db_mapping.DivisaoTreino)
                .where(
                    and_(
                        db_mapping.DivisaoTreino.divisao == division,
                        db_mapping.FichaTreino.id_usuario == user_id,
                        # Join
                        db_mapping.DivisaoTreino.id_ficha_treino
                        == db_mapping.FichaTreino.id_ficha_treino,
                    )
                )
                .values(divisao=new_division_name)
                .returning(db_mapping.FichaTreino.id_ficha_treino)
            )
        except IntegrityError as exc:
            await session.rollback()

            if "pk_divisao_treino" in str(exc):
                raise HTTPException(
                    CONFLICT, "Já existe essa divisão nessa ficha de treino"
                )

            if "fk_fivisao_treino_ficha_treino" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "O ID da ficha de treino recebido não existe"
                )
        else:
            if result.scalar_one_or_none() is None:
                raise HTTPException(NOT_FOUND, "Divisão de treino não encontrada")
            await session.commit()


@DATA_PUT_API.put("/workout/division/exercise/update/")
async def update_division_exercise(
    updates: schemas.DivisaoExercicioAlterar,
    user_id: int = Depends(TokenService.validate_token),
):
    async with AsyncSession() as session:
        try:
            result = await session.execute(
                update(db_mapping.DivisaoExercicio)
                .where(
                    and_(
                        db_mapping.DivisaoExercicio.divisao == updates.divisao,
                        db_mapping.DivisaoExercicio.id_exercicio == updates.id_exercicio,
                        db_mapping.DivisaoExercicio.ordem_execucao
                        == updates.ordem_execucao_atual,
                        db_mapping.FichaTreino.id_usuario == user_id,
                        db_mapping.FichaTreino.id_ficha_treino == updates.id_ficha_treino,
                        # Joins
                        db_mapping.DivisaoExercicio.id_ficha_treino
                        == db_mapping.DivisaoTreino.id_ficha_treino,
                        db_mapping.DivisaoTreino.id_ficha_treino
                        == db_mapping.FichaTreino.id_ficha_treino,
                    )
                )
                .values(
                    updates.model_dump(
                        exclude=(
                            "ordem_execucao_atual",
                            "id_ficha_treino",
                            "id_exercicio",
                            "divisao",
                        )
                    )
                )
                .returning(db_mapping.FichaTreino.id_ficha_treino)
            )

        except IntegrityError as exc:
            if "pk_divisao_exercicio" in str(exc):
                raise HTTPException(CONFLICT, "Esse exercício já existe nessa divisão")

            if "fk_divisao_exercicio_divisao_treino" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "A divisão de treino referenciada não existe"
                )
        else:
            if result.scalar_one_or_none() is None:
                raise HTTPException(NOT_FOUND, "Exercício não encontrado nessa divisão")
            await session.commit()

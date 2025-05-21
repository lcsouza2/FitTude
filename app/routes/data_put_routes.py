from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import and_, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import InstrumentedAttribute, MappedAsDataclass
from sqlalchemy.sql.expression import BinaryExpression

from app.core import schemas
from app.core.authentication import TokenService
from app.core.connections import db_connection
from app.core.exceptions import (
    EntityNotFound,
    ForeignKeyViolation,
    PrimaryKeyViolation,
    UniqueConstraintViolation,
)
from app.core.utils import exclude_falsy_from_dict
from app.database import db_mapping

DATA_PUT_API = APIRouter(prefix="/api/data", tags=["Data Put Routes"])


async def _execute_update(
    *,
    table: MappedAsDataclass,
    entity_name: str,
    where_clause: BinaryExpression,
    values_mapping: Dict[InstrumentedAttribute, Any],
    error_mapping: List[schemas.ConstraintErrorHandling],
    returning_column: Optional[InstrumentedAttribute] = None,
):
    """
    Executa uma operação de atualização genérica no banco de dados.

    Args:
        table: Classe do modelo SQLAlchemy a ser atualizado
        entity_name: Nome da entidade para mensagens de erro
        where_clause: Condição WHERE da query
        values_mapping: Dicionário com os valores a serem atualizados
        error_mapping: Lista de mapeamentos de erros de constraint
        returning_column: Coluna a ser retornada após atualização

    Returns:
        str: Mensagem de sucesso "Alterado"

    Raises:
        EntityNotFound: Se o registro não for encontrado
        IntegrityError: Para violações de constraint do banco
    """
    async with await db_connection() as session:
        try:
            result = await session.execute(
                update(table)
                .where(where_clause)
                .values(values_mapping)
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


@DATA_PUT_API.put("/groups/update/{group_name}")
async def update_group(
    group_name: str,
    updates: schemas.UpdateMuscleGroup,
    user_id: int = Depends(TokenService.validate_token),
):
    """Update an existing muscle group"""
    await _execute_update(
        table=db_mapping.MuscleGroup,
        entity_name="Muscle Group",
        where_clause=and_(
            db_mapping.MuscleGroup.group_name == group_name,
            db_mapping.MuscleGroup.user_id == user_id,
        ),
        values_mapping=exclude_falsy_from_dict(updates.model_dump(exclude_none=True)),
        error_mapping=[
            {
                "constraint": "uq_muscle_group",
                "error": UniqueConstraintViolation,
                "message": "Data conflicts with an existing record",
            },
            {
                "constraint": "fk_muscle_group_user",
                "error": ForeignKeyViolation,
                "message": "Referenced user not found",
            },
        ],
        returning_column=db_mapping.MuscleGroup.group_name,
    )


@DATA_PUT_API.put("/muscle/update/{muscle_id}")
async def update_muscle(
    muscle_id: int,
    updates: schemas.UpdateMuscle,
    user_id: int = Depends(TokenService.validate_token),
):
    await _execute_update(
        table=db_mapping.Muscle,
        entity_name="Muscle",
        where_clause=and_(
            db_mapping.Muscle.muscle_id == muscle_id,
            db_mapping.Muscle.user_id == user_id,
        ),
        values_mapping=exclude_falsy_from_dict(updates.model_dump(exclude_none=True)),
        error_mapping=[
            {
                "constraint": "uq_muscle",
                "error": UniqueConstraintViolation,
                "message": "Data conflicts with an existing record",
            },
            {
                "constraint": "fk_muscle_muscle_group",
                "error": ForeignKeyViolation,
                "message": "Referenced muscle group not found",
            },
            {
                "constraint": "fk_muscle_user",
                "error": ForeignKeyViolation,
                "message": "Referenced user not found",
            },
        ],
        returning_column=db_mapping.Muscle.muscle_id,
    )


@DATA_PUT_API.put("/equipment/update/{equipment_id}")
async def update_equipment(
    equipment_id: int,
    updates: schemas.UpdateEquipment,
    user_id: int = Depends(TokenService.validate_token),
):
    await _execute_update(
        table=db_mapping.Equipment,
        entity_name="Equipment",
        where_clause=and_(
            db_mapping.Equipment.equipment_id == equipment_id,
            db_mapping.Equipment.user_id == user_id,
        ),
        values_mapping=exclude_falsy_from_dict(updates.model_dump(exclude_none=True)),
        error_mapping=[
            {
                "constraint": "uq_equipment",
                "error": UniqueConstraintViolation,
                "message": "Data conflicts with an existing record",
            },
            {
                "constraint": "fk_equipment_muscle_group",
                "error": ForeignKeyViolation,
                "message": "Referenced muscle group not found",
            },
            {
                "constraint": "fk_equipment_user",
                "error": ForeignKeyViolation,
                "message": "Referenced user not found",
            },
        ],
        returning_column=db_mapping.Equipment.equipment_id,
    )


@DATA_PUT_API.put("/exercise/update/{exercise_id}")
async def update_exercise(
    exercise_id: int,
    updates: schemas.UpdateExercise,
    user_id: int = Depends(TokenService.validate_token),
):
    await _execute_update(
        table=db_mapping.Exercise,
        entity_name="Exercise",
        where_clause=and_(
            db_mapping.Exercise.exercise_id == exercise_id,
            db_mapping.Exercise.user_id == user_id,
        ),
        values_mapping=exclude_falsy_from_dict(updates.model_dump(exclude_none=True)),
        error_mapping=[
            {
                "constraint": "uq_exercise",
                "error": UniqueConstraintViolation,
                "message": "Data conflicts with an existing record",
            },
            {
                "constraint": "fk_exercise_equipment",
                "error": ForeignKeyViolation,
                "message": "Referenced equipment not found",
            },
            {
                "constraint": "fk_exercise_muscle",
                "error": ForeignKeyViolation,
                "message": "Referenced muscle not found",
            },
            {
                "constraint": "fk_exercise_user",
                "error": ForeignKeyViolation,
                "message": "Referenced user not found",
            },
        ],
        returning_column=db_mapping.Exercise.exercise_id,
    )


@DATA_PUT_API.put("/workout/plan/update/{plan_id}")
async def update_workout_plan(
    plan_id: int,
    updates: schemas.UpdateWorkoutPlan,
    user_id: int = Depends(TokenService.validate_token),
):
    await _execute_update(
        table=db_mapping.WorkoutPlan,
        entity_name="Workout Plan",
        where_clause=and_(
            db_mapping.WorkoutPlan.workout_plan_id == plan_id,
            db_mapping.WorkoutPlan.user_id == user_id,
        ),
        values_mapping=exclude_falsy_from_dict(updates.model_dump(exclude_none=True)),
        error_mapping=[
            {
                "constraint": "uq_workout_plan",
                "error": UniqueConstraintViolation,
                "message": "Data conflicts with an existing record",
            },
            {
                "constraint": "fk_workout_plan_user",
                "error": ForeignKeyViolation,
                "message": "Referenced user not found",
            },
        ],
        returning_column=db_mapping.WorkoutPlan.workout_plan_id,
    )


@DATA_PUT_API.put("/workout/split/exercise/update/")
async def update_split_exercise(
    updates: schemas.UpdateSplitExercise,
    user_id: int = Depends(TokenService.validate_token),
):
    where_query = and_(
        db_mapping.SplitExercise.split == updates.split,
        db_mapping.SplitExercise.exercise_id == updates.exercise_id,
        db_mapping.SplitExercise.execution_order == updates.current_execution_order,
        db_mapping.WorkoutPlan.user_id == user_id,
        db_mapping.WorkoutPlan.workout_plan_id == updates.workout_plan_id,
        # Joins
        db_mapping.SplitExercise.workout_plan_id
        == db_mapping.WorkoutSplit.workout_plan_id,
        db_mapping.WorkoutSplit.workout_plan_id
        == db_mapping.WorkoutPlan.workout_plan_id,
    )

    update_values = updates.model_dump(
        exclude=(
            "current_execution_order",
            "workout_plan_id",
            "exercise_id",
            "split",
        )
    )

    await _execute_update(
        table=db_mapping.SplitExercise,
        entity_name="Split Exercise",
        where_clause=where_query,
        values_mapping=update_values,
        error_mapping=[
            {
                "constraint": "pk_split_exercise",
                "error": PrimaryKeyViolation,
                "message": "Exercise already exists in this split",
            },
            {
                "constraint": "fk_split_exercise_workout_split",
                "error": ForeignKeyViolation,
                "message": "Referenced workout split not found",
            },
        ],
        returning_column=db_mapping.WorkoutPlan.workout_plan_id,
    )

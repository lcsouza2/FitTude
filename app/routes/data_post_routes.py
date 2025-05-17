from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import MappedAsDataclass

from app.core import schemas
from app.core.authentication import TokenService
from app.core.connections import AsyncSession
from app.core.exceptions import (
    ForeignKeyViolation,
    PrimaryKeyViolation,
    UniqueConstraintViolation,
)
from app.core.utils import exclude_falsy_from_dict

from app.database import db_mapping

DATA_POST_API = APIRouter(prefix="/api/data", tags=["Data Post Routes"])


async def _execute_insert(
    *,
    table: MappedAsDataclass,
    values: Dict[str, Any],
    error_mapping: List[schemas.ConstraintErrorHandling],
    entity_name: str,
) -> str:
    """
    Executes a generic insert operation in the database.

    Args:
        table: SQLAlchemy model class to insert into
        values: Dictionary with the values to insert
        error_mapping: List of dictionaries mapping database constraints to errors
        entity_name: Name of the entity for error messages

    Returns:
        str: Success message

    Raises:
        HTTPException: For database constraint violations
    """
    async with AsyncSession() as session:
        try:
            await session.execute(insert(table).values(values))
            await session.commit()
            return f"{entity_name} created successfully"

        except IntegrityError as exc:
            await session.rollback()
            for error in error_mapping:
                if error.get("constraint") in str(exc):
                    raise error.get("error")(error.get("message"))
            # If no mapped error is found, re-raise the original exception
            raise


@DATA_POST_API.post("/groups/new")
async def create_new_group(
    group: schemas.Musclegroup, user_id: int = Depends(TokenService.validate_token)
):
    """Add a new muscle group"""
    return await _execute_insert(
        table=db_mapping.MuscleGroup,
        values={**group.model_dump(), "user_id": user_id},
        error_mapping=[
            {
                "constraint": "uq_muscle_group",
                "error": UniqueConstraintViolation,
                "message": "This muscle group already exists",
            },
            {
                "constraint": "fk_muscle_group_user",
                "error": ForeignKeyViolation,
                "message": "Referenced user not found",
            },
        ],
        entity_name="Muscle Group",
    )


@DATA_POST_API.post("/equipment/new")
async def create_new_equipment(
    equipment: schemas.Equipment, user_id: int = Depends(TokenService.validate_token)
):
    """Create new equipment"""
    return await _execute_insert(
        table=db_mapping.Equipment,
        values={**equipment.model_dump(), "user_id": user_id},
        error_mapping=[
            {
                "constraint": "uq_equipment",
                "error": UniqueConstraintViolation,
                "message": "This equipment already exists",
            },
            {
                "constraint": "fk_equipment_user",
                "error": ForeignKeyViolation,
                "message": "Referenced user not found",
            },
            {
                "constraint": "fk_equipment_muscle_group",
                "error": ForeignKeyViolation,
                "message": "Referenced muscle group not found",
            },
        ],
        entity_name="Equipment",
    )


@DATA_POST_API.post("/muscle/new")
async def create_new_muscle(
    muscle: schemas.Muscle, user_id: int = Depends(TokenService.validate_token)
):
    """Add a new muscle"""
    return await _execute_insert(
        table=db_mapping.Muscle,
        values={**muscle.model_dump(), "user_id": user_id},
        error_mapping=[
            {
                "constraint": "uq_muscle",
                "error": UniqueConstraintViolation,
                "message": "This muscle already exists",
            },
            {
                "constraint": "fk_muscle_user",
                "error": ForeignKeyViolation,
                "message": "Referenced user not found",
            },
            {
                "constraint": "fk_muscle_muscle_group",
                "error": ForeignKeyViolation,
                "message": "Referenced muscle group not found",
            },
        ],
        entity_name="Muscle",
    )


@DATA_POST_API.post("/exercise/new")
async def create_new_exercise(
    exercise: schemas.Exercise, user_id: int = Depends(TokenService.validate_token)
):
    """Add a new exercise"""
    return await _execute_insert(
        table=db_mapping.Exercise,
        values={**exercise.model_dump(), "user_id": user_id},
        error_mapping=[
            {
                "constraint": "uq_exercise",
                "error": UniqueConstraintViolation,
                "message": "This exercise already exists",
            },
            {
                "constraint": "fk_exercise_user",
                "error": ForeignKeyViolation,
                "message": "Referenced user not found",
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
        ],
        entity_name="Exercise",
    )


@DATA_POST_API.post("/workout/plan/new")
async def create_new_workout_plan(
    plan: schemas.WorkoutPlan, user_id: int = Depends(TokenService.validate_token)
):
    """Create a new workout plan"""
    return await _execute_insert(
        table=db_mapping.WorkoutPlan,
        values={**plan.model_dump(), "user_id": user_id},
        error_mapping=[
            {
                "constraint": "uq_workout_plan",
                "error": UniqueConstraintViolation,
                "message": "This workout plan already exists",
            },
            {
                "constraint": "fk_workout_plan_user",
                "error": ForeignKeyViolation,
                "message": "Referenced user not found",
            },
        ],
        entity_name="Workout Plan",
    )


@DATA_POST_API.post("/workout/split/new")
async def create_new_workout_split(
    split: schemas.WorkoutSplit, user_id: int = Depends(TokenService.validate_token)
):
    """Create a new workout split"""
    return await _execute_insert(
        table=db_mapping.WorkoutSplit,
        values=split.model_dump(),
        error_mapping=[
            {
                "constraint": "pk_workout_split",
                "error": PrimaryKeyViolation,
                "message": "This workout split already exists in the plan",
            },
            {
                "constraint": "fk_workout_split_workout_plan",
                "error": ForeignKeyViolation,
                "message": "Referenced workout plan not found",
            },
        ],
        entity_name="Workout Split",
    )


@DATA_POST_API.post("/workout/split/add_exercise")
async def add_exercise_to_split(
    exercises: List[schemas.SplitExercise],
    user_id: int = Depends(TokenService.validate_token),
):
    """Add a list of exercises to a workout split"""
    await _execute_insert(
        table=db_mapping.SplitExercise,
        values=[i.model_dump() for i in exercises],
        error_mapping=[
            {
                "constraint": "pk_split_exercise",
                "error": PrimaryKeyViolation,
                "message": "This exercise already exists in the split",
            },
            {
                "constraint": "fk_split_exercise_workout_split",
                "error": ForeignKeyViolation,
                "message": "Referenced workout split not found",
            },
            {
                "constraint": "fk_split_exercise_exercise",
                "error": ForeignKeyViolation,
                "message": "Referenced exercise not found",
            },
        ],
        entity_name="Split Exercise",
    )


@DATA_POST_API.post("/workout/report/new")
async def create_new_workout_report(
    report: schemas.WorkoutReport, user_id: int = Depends(TokenService.validate_token)
):
    """Create a new workout report"""
    return await _execute_insert(
        table=db_mapping.WorkoutReport,
        values=report.model_dump(),
        error_mapping=[
            {
                "constraint": "fk_workout_report_workout_split",
                "error": ForeignKeyViolation,
                "message": "Referenced workout split not found",
            },
        ],
        entity_name="Workout Report",
    )


@DATA_POST_API.post("/workout/report/add_set")
async def add_set_to_report(
    sets: List[schemas.SetReport],
    user_id: int = Depends(TokenService.validate_token),
):
    """Add a list of sets to a workout report"""
    await _execute_insert(
        table=db_mapping.SetReport,
        values=[
            exclude_falsy_from_dict(i.model_dump(exclude_none=True)) for i in sets
        ],
        error_mapping=[
            {
                "constraint": "pk_set_report",
                "error": PrimaryKeyViolation,
                "message": "This set already exists in the report",
            },
            {
                "constraint": "fk_set_report_split_exercise",
                "error": ForeignKeyViolation,
                "message": "Referenced split exercise not found",
            },
            {
                "constraint": "fk_set_report_workout_report",
                "error": ForeignKeyViolation,
                "message": "Referenced workout report not found",
            },
        ],
        entity_name="Set Report",
    )

from fastapi import APIRouter, Depends
from sqlalchemy import BinaryExpression, and_, delete, update
from sqlalchemy.orm import InstrumentedAttribute, MappedAsDataclass

from ..core import schemas
from ..core.authentication import TokenService
from ..core.connections import db_connection
from ..core.exceptions import EntityNotFound

from ..database import db_mapping

DATA_DELETE_API = APIRouter(prefix="/api/data", tags=["Data Delete Routes"])


async def _execute_inactivate_entity(
    *,
    table: MappedAsDataclass,
    where_clause: BinaryExpression,
    returning_column: InstrumentedAttribute,
    entity_name: str,
):
    async with db_connection() as session:
        result = await session.execute(
            update(table)
            .values(active=False)
            .where(where_clause)
            .returning(returning_column)
        )

        if result.scalar_one_or_none() is None:
            await session.rollback()
            raise EntityNotFound(f"{entity_name} not found")

        await session.commit()

        return f"{entity_name} inactivated successfully"


async def _execute_delete(
    *,
    table: MappedAsDataclass,
    where_clause: BinaryExpression,
    returning_column: InstrumentedAttribute,
    entity_name: str,
):
    async with db_connection() as session:
        result = await session.execute(
            delete(table).where(where_clause).returning(returning_column)
        )

        if result.scalar_one_or_none() is None:
            await session.rollback()
            raise EntityNotFound(f"{entity_name} not found")

        await session.commit()

        return f"{entity_name} deleted successfully"


@DATA_DELETE_API.delete("/groups/inactivate/{group_name}")
async def inactivate_group(
    group_name: str, user_id: int = Depends(TokenService.validate_token)
):
    """Inactivate a muscle group"""
    where = and_(
        db_mapping.MuscleGroup.group_name == group_name,
        db_mapping.MuscleGroup.user_id == user_id,
    )

    returning = db_mapping.MuscleGroup.group_name

    await _execute_inactivate_entity(
        table=db_mapping.MuscleGroup,
        where_clause=where,
        returning_column=returning,
        entity_name="Muscle Group",
    )


@DATA_DELETE_API.delete("/muscle/inactivate/{muscle_id}")
async def inactivate_muscle(
    muscle_id: int, user_id: int = Depends(TokenService.validate_token)
):
    where = and_(
        db_mapping.Musculo.id_musculo == muscle_id,
        db_mapping.Musculo.user_id == user_id,
    )

    returning = db_mapping.Musculo.id_musculo

    await _execute_inactivate_entity(
        table=db_mapping.Musculo,
        where_clause=where,
        returning_column=returning,
        entity_name="Musculo",
    )


@DATA_DELETE_API.delete("/equipment/inactivate/{equipment_id}")
async def inactivate_equipment(
    equipment_id: int, user_id: int = Depends(TokenService.validate_token)
):
    where = and_(
        db_mapping.Aparelho.id_aparelho == equipment_id,
        db_mapping.Aparelho.user_id == user_id,
    )

    returning = db_mapping.Aparelho.id_aparelho

    await _execute_inactivate_entity(
        table=db_mapping.Aparelho,
        where_clause=where,
        returning_column=returning,
        entity_name="Aparelho",
    )


@DATA_DELETE_API.delete("/exericse/inactivate/{exercise_id}")
async def inactivate_exercise(
    exercise_id: int, user_id: int = Depends(TokenService.validate_token)
):
    where = and_(
        db_mapping.Exercise.exercise_id == exercise_id,
        db_mapping.Exercise.user_id == user_id,
    )

    returning = db_mapping.Exercise.exercise_id

    await _execute_inactivate_entity(
        table=db_mapping.Exercise,
        where_clause=where,
        returning_column=returning,
        entity_name="Exercício",
    )


@DATA_DELETE_API.delete("/workout/sheet/inactivate/{sheet_id}")
async def inactivate_workout_sheet(
    sheet_id: int, user_id: int = Depends(TokenService.validate_token)
):
    where = and_(
        db_mapping.WorkoutPlan.workout_plan_id == sheet_id,
        db_mapping.WorkoutPlan.user_id == user_id,
    )

    returning = db_mapping.WorkoutPlan.workout_plan_id

    await _execute_inactivate_entity(
        table=db_mapping.WorkoutPlan,
        where_clause=where,
        returning_column=returning,
        entity_name="Ficha de treino",
    )


@DATA_DELETE_API.delete("/workout/split/inactivate/{split}")
async def inactivate_workout_split(
    split: str, user_id: int = Depends(TokenService.validate_token)
):
    where = and_(
        db_mapping.WorkoutSplit.split == split,
        db_mapping.WorkoutSplit.workout_plan_id
        == db_mapping.WorkoutPlan.workout_plan_id,
        db_mapping.WorkoutPlan.user_id == user_id,
    )

    returning = db_mapping.WorkoutPlan.workout_plan_id

    await _execute_inactivate_entity(
        table=db_mapping.WorkoutSplit,
        where_clause=where,
        returning_column=returning,
        entity_name="Divisão de treino",
    )


@DATA_DELETE_API.delete("/workout/split/exercise/inactivate")
async def inactivate_division_exercise(
    exercise: schemas.InactivateSplitExercise,
    user_id: int = Depends(TokenService.validate_token),
):
    where = and_(
        db_mapping.SplitExercise.split == exercise.split,
        db_mapping.SplitExercise.exercise_id == exercise.exercise_id,
        db_mapping.SplitExercise.execution_order == exercise.execution_order,
        db_mapping.WorkoutPlan.user_id == user_id,
        db_mapping.WorkoutPlan.workout_plan_id == exercise.workout_plan_id,
        # Joins
        db_mapping.SplitExercise.workout_plan_id
        == db_mapping.WorkoutSplit.workout_plan_id,
        db_mapping.WorkoutSplit.workout_plan_id
        == db_mapping.WorkoutPlan.workout_plan_id,
    )

    returning = db_mapping.WorkoutPlan.workout_plan_id

    await _execute_inactivate_entity(
        table=db_mapping.SplitExercise,
        where_clause=where,
        returning_column=returning,
        entity_name="Exercício na split de treino",
    )


@DATA_DELETE_API.delete("/workout/split/exercise/inactivate")
async def inactivate_split_exercise(
    exercise: schemas.InactivateSplitExercise,
    user_id: int = Depends(TokenService.validate_token),
):
    where = and_(
        db_mapping.SplitExercise.split == exercise.split,
        db_mapping.SplitExercise.exercise_id == exercise.exercise_id,
        db_mapping.SplitExercise.execution_order == exercise.execution_order,
        db_mapping.WorkoutPlan.user_id == user_id,
        db_mapping.WorkoutPlan.workout_plan_id == exercise.workout_plan_id,
        # Joins
        db_mapping.SplitExercise.workout_plan_id == db_mapping.WorkoutSplit.workout_plan_id,
        db_mapping.WorkoutSplit.workout_plan_id == db_mapping.WorkoutPlan.workout_plan_id,
    )

    returning = db_mapping.WorkoutPlan.workout_plan_id

    await _execute_inactivate_entity(
        table=db_mapping.SplitExercise,
        where_clause=where,
        returning_column=returning,
        entity_name="WorkoutSplit Exercise",
    )


@DATA_DELETE_API.delete("/workout/report/delete/{report_id}")
async def delete_workout_report(
    report_id: int, user_id: int = Depends(TokenService.validate_token)
):
    # First delete the set reports
    where_sets = and_(
        db_mapping.SetReport.workout_report_id == report_id,
        db_mapping.WorkoutPlan.user_id == user_id,
        # Joins
        db_mapping.SetReport.workout_report_id == db_mapping.WorkoutReport.workout_report_id,
        db_mapping.WorkoutReport.workout_plan_id == db_mapping.WorkoutPlan.workout_plan_id,
    )

    await _execute_delete(
        table=db_mapping.SetReport,
        where_clause=where_sets,
        returning_column=db_mapping.SetReport.workout_report_id,
        entity_name="Set Reports",
    )

    # Then delete the workout report
    where_report = and_(
        db_mapping.WorkoutReport.workout_report_id == report_id,
        db_mapping.WorkoutPlan.user_id == user_id,
        # Join
        db_mapping.WorkoutReport.workout_plan_id == db_mapping.WorkoutPlan.workout_plan_id,
    )

    await _execute_delete(
        table=db_mapping.WorkoutReport,
        where_clause=where_report,
        returning_column=db_mapping.WorkoutReport.workout_report_id,
        entity_name="Workout Report",
    )

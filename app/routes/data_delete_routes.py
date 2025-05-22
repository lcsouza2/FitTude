from fastapi import APIRouter, Depends, Query
from sqlalchemy import BinaryExpression, and_, delete, update
from sqlalchemy.orm import InstrumentedAttribute, MappedAsDataclass

from ..core import schemas
from ..core.authentication import TokenService
from ..core.connections import db_connection
from ..core.exceptions import EntityNotFound
from ..database import db_mapping

DATA_DELETE_ROUTER = APIRouter(prefix="/api/data", tags=["Data Delete Routes"])


async def _execute_inactivate_entity(
    *,
    table: MappedAsDataclass,
    where_clause: BinaryExpression,
    returning_column: InstrumentedAttribute,
    entity_name: str,
):
    """
    Executes a soft delete operation by setting the 'active' field to False for a given entity.

    This helper function handles the database transaction to inactivate (soft delete) an entity
    while maintaining referential integrity.

    Args:
        table (MappedAsDataclass): The SQLAlchemy table/model class to update
        where_clause (BinaryExpression): The SQLAlchemy where clause to filter records
        returning_column (InstrumentedAttribute): The column to return after update for verification
        entity_name (str): Display name of the entity for error/success messages

    Returns:
        str: Success message confirming entity inactivation

    Raises:
        EntityNotFound: If no matching record is found to inactivate
    """

    async with await db_connection() as session:
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
    """
    Executes a hard delete operation for a given entity in the database.

    This helper function handles the database transaction to permanently delete records
    while maintaining referential integrity. It performs a hard delete rather than a soft delete.

    Args:
        table (MappedAsDataclass): The SQLAlchemy table/model class to delete from
        where_clause (BinaryExpression): The SQLAlchemy where clause to filter records for deletion
        returning_column (InstrumentedAttribute): The column to return after deletion for verification
        entity_name (str): Display name of the entity for error/success messages

    Returns:
        str: Success message confirming entity deletion

    Raises:
        EntityNotFound: If no matching record is found to delete
    """

    async with await db_connection() as session:
        result = await session.execute(
            delete(table).where(where_clause).returning(returning_column)
        )

        if result.scalar_one_or_none() is None:
            await session.rollback()
            raise EntityNotFound(f"{entity_name} not found")

        await session.commit()

        return f"{entity_name} deleted successfully"


@DATA_DELETE_ROUTER.delete("/groups/inactivate/{group_name}")
async def inactivate_group(
    group_name: str, user_id: int = Depends(TokenService.validate_token)
):
    """
    Inactivates (soft deletes) a muscle group for a specific user.

    This endpoint performs a soft delete operation on a muscle group by setting its 'active' 
    field to False. The operation is scoped to the authenticated user to ensure data isolation.

    Args:
        group_name (str): The name of the muscle group to inactivate
        user_id (int): The ID of the authenticated user, obtained from the JWT token

    Returns:
        str: Success message confirming the muscle group was inactivated

    Raises:
        EntityNotFound: If no muscle group with the given name is found for the user
        HTTPException: If authentication fails or user lacks permissions
    """

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


@DATA_DELETE_ROUTER.delete("/muscle/inactivate/{muscle_id}")
async def inactivate_muscle(
    muscle_id: int, user_id: int = Depends(TokenService.validate_token)
):
    """
    Inactivates (soft deletes) a muscle for a specific user.

    Args:
        muscle_id (int): The ID of the muscle to inactivate
        user_id (int): The ID of the authenticated user, obtained from the JWT token

    Returns:
        str: Success message confirming the muscle was inactivated

    Raises:
        EntityNotFound: If no muscle with the given ID is found for the user
        HTTPException: If authentication fails or user lacks permissions
    """
    where = and_(
        db_mapping.Muscle.muscle_id == muscle_id,
        db_mapping.Muscle.user_id == user_id,
    )

    returning = db_mapping.Muscle.muscle_id

    await _execute_inactivate_entity(
        table=db_mapping.Muscle,
        where_clause=where,
        returning_column=returning,
        entity_name="Muscle",
    )


@DATA_DELETE_ROUTER.delete("/equipment/inactivate/{equipment_id}")
async def inactivate_equipment(
    equipment_id: int, user_id: int = Depends(TokenService.validate_token)
):
    """
    Inactivates (soft deletes) an equipment for a specific user.

    Args:
        equipment_id (int): The ID of the equipment to inactivate
        user_id (int): The ID of the authenticated user, obtained from the JWT token

    Returns:
        str: Success message confirming the equipment was inactivated

    Raises:
        EntityNotFound: If no equipment with the given ID is found for the user
        HTTPException: If authentication fails or user lacks permissions
    """
    where = and_(
        db_mapping.Equipment.equipment_id == equipment_id,
        db_mapping.Equipment.equipment_id == user_id,
    )

    returning = db_mapping.Equipment.equipment_id

    await _execute_inactivate_entity(
        table=db_mapping.Equipment,
        where_clause=where,
        returning_column=returning,
        entity_name="Equipment",
    )


@DATA_DELETE_ROUTER.delete("/exericse/inactivate/{exercise_id}")
async def inactivate_exercise(
    exercise_id: int, user_id: int = Depends(TokenService.validate_token)
):
    """
    Inactivates (soft deletes) an exercise for a specific user.

    Args:
        exercise_id (int): The ID of the exercise to inactivate
        user_id (int): The ID of the authenticated user, obtained from the JWT token

    Returns:
        str: Success message confirming the exercise was inactivated

    Raises:
        EntityNotFound: If no exercise with the given ID is found for the user
        HTTPException: If authentication fails or user lacks permissions
    """
    where = and_(
        db_mapping.Exercise.exercise_id == exercise_id,
        db_mapping.Exercise.user_id == user_id,
    )

    returning = db_mapping.Exercise.exercise_id

    await _execute_inactivate_entity(
        table=db_mapping.Exercise,
        where_clause=where,
        returning_column=returning,
        entity_name="Exercise",
    )


@DATA_DELETE_ROUTER.delete("/exercise/unbind_muscle")
async def unbind_muscle_exercise(
    bound_element: schemas.BindMuscleExecise,
    user_id: int = Depends(TokenService.validate_token)
):
    """
    Permanently deletes the association between a muscle and an exercise.
    This operation can only be performed by the owner of both the muscle and exercise.

    Args:
        bound_element (BindMuscleExecise): Schema containing exercise_id and muscle_id
        user_id (int): The ID of the authenticated user, obtained from the JWT token

    Returns:
        str: Success message confirming the association was deleted

    Raises:
        EntityNotFound: If no association is found or if user doesn't own both elements
        HTTPException: If authentication fails or user lacks permissions
    """
    where = and_(
        db_mapping.ExerciseMuscle.exercise_id == bound_element.exercise_id,
        db_mapping.ExerciseMuscle.muscle_id == bound_element.muscle_id,
        db_mapping.Exercise.user_id == user_id,
        db_mapping.Muscle.user_id == user_id,
        # Joins to verify ownership
        db_mapping.ExerciseMuscle.exercise_id == db_mapping.Exercise.exercise_id,
        db_mapping.ExerciseMuscle.muscle_id == db_mapping.Muscle.muscle_id,
    )

    returning = db_mapping.ExerciseMuscle.exercise_id

    return await _execute_delete(
        table=db_mapping.ExerciseMuscle,
        where_clause=where,
        returning_column=returning,
        entity_name="Muscle-Exercise association",
    )

@DATA_DELETE_ROUTER.delete("/exercise/unbind_equipment")
async def unbind_equipment_exercise(

    bound_element: schemas.BindEquipmentExecise,
    user_id: int = Depends(TokenService.validate_token)
):
    """
    Permanently deletes the association between an equipment and an exercise.

    This operation can only be performed by the owner of both the equipment and exercise.

    Args:
        bound_element (BindEquipmentExecise): Schema containing exercise_id and equipment_id
            for the association to be removed
        user_id (int): The ID of the authenticated user, obtained from the JWT token

    Returns:
        str: Success message confirming the association was deleted

    Raises:
        EntityNotFound: If no association is found or if user doesn't own both elements
        HTTPException: If authentication fails or user lacks permissions
    """


    where = and_(
        db_mapping.ExerciseEquipment.exercise_id == bound_element.exercise_id,
        db_mapping.ExerciseEquipment.equipment_id == bound_element.equipment_id,
        db_mapping.Exercise.user_id == user_id,
        db_mapping.Equipment.user_id == user_id,
        # Joins to verify ownership
        db_mapping.ExerciseEquipment.exercise_id == db_mapping.Exercise.exercise_id,
        db_mapping.ExerciseEquipment.equipment_id == db_mapping.Equipment.equipment_id,
    )

    returning = db_mapping.ExerciseEquipment.exercise_id

    return await _execute_delete(
        table=db_mapping.ExerciseEquipment,
        where_clause=where,
        returning_column=returning,
        entity_name="Exercise-Equipment association",
    )


@DATA_DELETE_ROUTER.delete("/workout/sheet/inactivate/{sheet_id}")
async def inactivate_workout_sheet(
    sheet_id: int, user_id: int = Depends(TokenService.validate_token)
):
    """
    Inactivates (soft deletes) a workout sheet for a specific user.

    Args:
        sheet_id (int): The ID of the workout sheet to inactivate
        user_id (int): The ID of the authenticated user, obtained from the JWT token

    Returns:
        str: Success message confirming the workout sheet was inactivated

    Raises:
        EntityNotFound: If no workout sheet with the given ID is found for the user
        HTTPException: If authentication fails or user lacks permissions
    """
    where = and_(
        db_mapping.WorkoutPlan.workout_plan_id == sheet_id,
        db_mapping.WorkoutPlan.user_id == user_id,
    )

    returning = db_mapping.WorkoutPlan.workout_plan_id

    await _execute_inactivate_entity(
        table=db_mapping.WorkoutPlan,
        where_clause=where,
        returning_column=returning,
        entity_name="Workout plan",
    )


@DATA_DELETE_ROUTER.delete("/workout/split/inactivate/{split}")
async def inactivate_workout_split(
    split: str, user_id: int = Depends(TokenService.validate_token)
):
    """
    Inactivates (soft deletes) a workout split for a specific user.

    Args:
        split (str): The name of the split to inactivate
        user_id (int): The ID of the authenticated user, obtained from the JWT token

    Returns:
        str: Success message confirming the workout split was inactivated

    Raises:
        EntityNotFound: If no workout split with the given name is found for the user
        HTTPException: If authentication fails or user lacks permissions
    """
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
        entity_name="Workout Split",
    )


@DATA_DELETE_ROUTER.delete("/workout/split/exercise/inactivate")
async def inactivate_division_exercise(
    exercise: schemas.InactivateSplitExercise,
    user_id: int = Depends(TokenService.validate_token),
):
    """
    Inactivates (soft deletes) an exercise from a workout split.

    Args:
        exercise (InactivateSplitExercise): The exercise details to inactivate
        user_id (int): The ID of the authenticated user, obtained from the JWT token

    Returns:
        str: Success message confirming the split exercise was inactivated

    Raises:
        EntityNotFound: If no matching exercise is found in the split
        HTTPException: If authentication fails or user lacks permissions
    """
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
        entity_name="Split Exercise",
    )


@DATA_DELETE_ROUTER.delete("/workout/split/exercise/inactivate")
async def inactivate_split_exercise(
    exercise: schemas.InactivateSplitExercise,
    user_id: int = Depends(TokenService.validate_token),
):
    """
    Inactivates (soft deletes) an exercise from a workout split.

    Args:
        exercise (InactivateSplitExercise): Schema containing split, exercise_id, execution_order 
            and workout_plan_id
        user_id (int): The ID of the authenticated user, obtained from the JWT token

    Returns:
        str: Success message confirming the split exercise was inactivated

    Raises:
        EntityNotFound: If no matching exercise is found in the split
        HTTPException: If authentication fails or user lacks permissions
    """
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
        entity_name="WorkoutSplit Exercise",
    )


@DATA_DELETE_ROUTER.delete("/workout/report/delete/{report_id}")
async def delete_workout_report(
    report_id: int, user_id: int = Depends(TokenService.validate_token)
):
    """
    Permanently deletes a workout report and its associated set reports.
    This operation cannot be undone.

    Args:
        report_id (int): The ID of the workout report to delete
        user_id (int): The ID of the authenticated user, obtained from the JWT token

    Returns:
        str: Success message confirming the workout report and associated sets were deleted

    Raises:
        EntityNotFound: If no workout report with the given ID is found for the user
        HTTPException: If authentication fails or user lacks permissions
    """
    # First delete the set reports
    where_sets = and_(
        db_mapping.SetReport.workout_report_id == report_id,
        db_mapping.WorkoutPlan.user_id == user_id,
        # Joins
        db_mapping.SetReport.workout_report_id
        == db_mapping.WorkoutReport.workout_report_id,
        db_mapping.WorkoutReport.workout_plan_id
        == db_mapping.WorkoutPlan.workout_plan_id,
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
        db_mapping.WorkoutReport.workout_plan_id
        == db_mapping.WorkoutPlan.workout_plan_id,
    )

    await _execute_delete(
        table=db_mapping.WorkoutReport,
        where_clause=where_report,
        returning_column=db_mapping.WorkoutReport.workout_report_id,
        entity_name="Workout Report",
    )

from typing import Any, Dict, List

from fastapi import APIRouter, Depends, Query
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
    MissingParameters
)
from app.core.utils import exclude_falsy_from_dict

from app.database import db_mapping

DATA_POST_API = APIRouter(prefix="/api/data", tags=["Data Post Routes"])


async def _execute_insert(
    *,
    table: MappedAsDataclass,
    values: Dict[str, Any],
    error_mapping: List[schemas.ConstraintErrorHandling],
    sucess_message: str,
) -> str:
    """
    Executes a generic insert operation in the database.

    Args:
        table: SQLAlchemy model class to insert into
        values: Dictionary with the values to insert
        error_mapping: List of dictionaries mapping database constraints to errors
        success_message: Name of the entity for error messages

    Returns:
        str: Success message

    Raises:
        HTTPException: For database constraint violations
    """
    async with AsyncSession() as session:
        try:
            await session.execute(insert(table).values(values))
            await session.commit()
            return sucess_message

        except IntegrityError as exc:
            await session.rollback()
            for error in error_mapping:
                if error.get("constraint") in str(exc):
                    raise error.get("error")(error.get("message"))
            raise


@DATA_POST_API.post("/groups/new")
async def create_new_group(
    group: schemas.Musclegroup, user_id: int = Depends(TokenService.validate_token)
):
    """
    Create a new muscle group in the database.

    This endpoint allows users to create a new muscle group, which can be used to categorize
    muscles and equipment for exercise organization.

    Args:
        group (schemas.Musclegroup): The muscle group data to be created
        user_id (int): User ID for authentication (injected by FastAPI)

    Returns:
        str: Success message indicating the muscle group was created

    Raises:
        UniqueConstraintViolation: If a muscle group with the same name already exists
        ForeignKeyViolation: If the referenced user does not exist
    """
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
        success_message="Muscle Group created succefully!",
    )


@DATA_POST_API.post("/equipment/new")
async def create_new_equipment(
    equipment: schemas.Equipment, user_id: int = Depends(TokenService.validate_token)
):
    """
    Create a new equipment in the database.

    This endpoint allows users to create a new piece of equipment, which can be used to
    track different equipment used in exercises. Each equipment is associated with a muscle
    group and user.

    Args:
        equipment (schemas.Equipment): The equipment data to be created, containing name and 
            muscle group ID
        user_id (int): User ID for authentication (injected by FastAPI)

    Returns:
        str: Success message indicating the equipment was created

    Raises:
        UniqueConstraintViolation: If equipment with the same name already exists
        ForeignKeyViolation: If the referenced user or muscle group does not exist in the database
    """
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
        success_message="Equipment created succesfully",
    )


@DATA_POST_API.post("/muscle/new")
async def create_new_muscle(
    muscle: schemas.Muscle, user_id: int = Depends(TokenService.validate_token)
):
    """
    Create a new muscle in the database.

    This endpoint allows users to create a new muscle entry, associating it with a muscle group
    and the user who created it. Each muscle must be unique within the system.

    Args:
        muscle (schemas.Muscle): The muscle data to be created, containing name and muscle group ID
        user_id (int): User ID for authentication (injected by FastAPI)

    Returns:
        str: Success message indicating the muscle was created

    Raises:
        UniqueConstraintViolation: If a muscle with the same name already exists
        ForeignKeyViolation: If the referenced user or muscle group does not exist
    """
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
        success_message="Muscle created succesfully",
    )


@DATA_POST_API.post("/exercise/new")
async def create_new_exercise(
    exercise: schemas.Exercise, user_id: int = Depends(TokenService.validate_token)
):
    """
    Create a new exercise in the database.

    This endpoint allows users to create a new exercise entry, associating it with equipment,
    muscles, and the user who created it. Each exercise must be unique within the system.
    Args:
        exercise (schemas.Exercise): The exercise data to be created, containing name,
        description, and associated equipment/muscle IDs

        user_id (int): User ID for authentication (injected by FastAPI)

    Returns:
        str: Success message indicating the exercise was created

    Raises:
        UniqueConstraintViolation: If an exercise with the same name already exists
        ForeignKeyViolation: If any of the referenced entities (user, equipment, muscle)
            do not exist in the database
    """
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
        success_message="Exercise created succesfully",
    )

@DATA_POST_API.post("/exercise/bind_muscle")
async def bind_muscle_to_exercise(
    exercise_id: int = Query(default=None),
    muscle_id: int = Query(default=None),
    user_id: int = Depends(TokenService.validate_token)
): 
    """
    Bind a muscle to an exercise.

    This endpoint creates a relationship between an exercise and a muscle,
    specifying which muscles are worked during the exercise execution.

    Args:
        exercise_id (int): Exercise ID to bind
        muscle_id (int): Muscle ID to bind
        user_id (int): user_id for authentication (injected by FastAPI)

    Returns:
        str: success message

    Raises:
        MissingParameters: When exercise_id or equipment_id is not provided
        PrimaryKeyViolation: When the equipment is already bound to the exercise
        ForeignKeyViolation: When referenced exercise or equipment doesn't exist
    """
    if not exercise_id or not muscle_id:
        raise MissingParameters()

    return await _execute_insert(
        table=db_mapping.ExerciseMuscle,
        values={
            "exercise_id": exercise_id,
            "muscle_id": muscle_id
        },
        error_mapping=[
            {
                "constraint": "pk_exercise_muscle",
                "error": PrimaryKeyViolation,
                "message": "Muscle already binded to muscle",
            },
            {
                "constraint": "fk_exercise_muscle_muscle",
                "error": ForeignKeyViolation,
                "message": "Referenced muscle not found",
            },
            {
                "constraint": "fk_exercise_muscle_exercise",
                "error": ForeignKeyViolation,
                "message": "Referenced exercise not found",
            },
        ],
        succes_message="Muscle binded to exercise succesfully"
    )


@DATA_POST_API.post("/exercise/bind_equipment")
async def bind_equipment_to_exercise(
    exercise_id: int = Query(default=None, description="ID of the exercise to bind equipment to"),
    equipment_id: int = Query(default=None, description="ID of the equipment to bind"),
    user_id: int = Depends(TokenService.validate_token)
):
    """
    Bind equipment to an exercise.

    This endpoint creates a relationship between an exercise and a piece of equipment,
    allowing tracking of which equipment can be used for each exercise.

    Args:
        exercise_id (int): Exercise ID to bind
        equipment_id (int): Equipment ID to bind
        user_id (int): User ID for authentication (injected by FastAPI)
    Returns:
        str: Success message
    Raises:
        MissingParameters: When exercise_id or equipment_id is not provided
        PrimaryKeyViolation: When the equipment is already bound to the exercise
        ForeignKeyViolation: When referenced exercise or equipment doesn't exist
    """
    if not exercise_id or not equipment_id:
        raise MissingParameters("Both exercise_id and equipment_id are required")

    return await _execute_insert(
        table=db_mapping.ExerciseEquipment,
        values={
            "exercise_id": exercise_id,
            "equipment_id": equipment_id
        },
        error_mapping=[
            {
                "constraint": "pk_exercise_equipment",
                "error": PrimaryKeyViolation,
                "message": "Equipment already bound to this exercise",
            },
            {
                "constraint": "fk_exercise_equipment_equipment",
                "error": ForeignKeyViolation,
                "message": "Referenced equipment not found",
            },
            {
                "constraint": "fk_exercise_equipment_exercise",
                "error": ForeignKeyViolation,
                "message": "Referenced exercise not found",
            },
        ],
        success_message="Equipment bound to exercise successfully"
    )


@DATA_POST_API.post("/workout/plan/new")
async def create_new_workout_plan(
    
    plan: schemas.WorkoutPlan, user_id: int = Depends(TokenService.validate_token)
):

    """
    Create a new workout plan in the database.
    
    This endpoint allows users to create a new workout plan, which serves as a container for 
    workout splits and exercises. Each plan is unique and associated with the user who created it.
    
    Args:
        plan (schemas.WorkoutPlan): The workout plan data to be created, containing the plan details
        user_id (int): User ID for authentication (injected by FastAPI)
    
    Returns:
        str: Success message indicating the workout plan was created
    
    Raises:
        UniqueConstraintViolation: If a workout plan with the same name already exists for this user
        ForeignKeyViolation: If the referenced user does not exist in the database
    """

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
        success_message="Workout Plan",
    )


@DATA_POST_API.post("/workout/split/new")
async def create_new_workout_split(
    split: schemas.WorkoutSplit, user_id: int = Depends(TokenService.validate_token)
):

    """
    Create a new workout split in the database.

    This endpoint allows users to create a new workout split within a workout plan. A workout split 
    represents a specific training day or session within the overall workout plan (e.g., "Push Day", 
    "Pull Day", "Legs Day").

    Args:
        split (schemas.WorkoutSplit): The workout split data to be created, containing the split name,
            description and workout plan ID it belongs to
        user_id (int): User ID for authentication (injected by FastAPI)

    Returns:
        str: Success message indicating the workout split was created

    Raises:
        PrimaryKeyViolation: If a split with the same name already exists in the workout plan
        ForeignKeyViolation: If the referenced workout plan does not exist in the database
    """

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
        success_message="Workout Split",
    )


@DATA_POST_API.post("/workout/split/add_exercise")
async def bind_exercise_to_split(
    
    exercises: List[schemas.SplitExercise],
    user_id: int = Depends(TokenService.validate_token),
):

    """
    Add exercises to a workout split.

    This endpoint allows users to add one or more exercises to a workout split, defining the 
    exercises that should be performed in that specific training session. Each exercise addition
    includes details like sets, reps and rest time.

    Args:
        exercises (List[schemas.SplitExercise]): List of exercises to add to the split, containing
            exercise ID, workout split ID, and exercise details (sets, reps, rest time)
        user_id (int): User ID for authentication (injected by FastAPI)

    Returns:
        str: Success message indicating the exercises were added to the split

    Raises:
        PrimaryKeyViolation: If any exercise is already present in the split
        ForeignKeyViolation: If the referenced workout split or exercise doesn't exist in the database
    """

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
        success_message="Split Exercise",
    )


@DATA_POST_API.post("/workout/report/new")
async def create_new_workout_report(
    report: schemas.WorkoutReport, user_id: int = Depends(TokenService.validate_token)
):

    """
    Create a new workout report in the database.

    This endpoint allows users to create a new workout report, which tracks the execution of a workout
    split session. The report serves as a container for recording sets, reps, weights and other 
    training details performed during a workout.

    Args:
        report (schemas.WorkoutReport): The workout report data to be created, containing the workout
            split ID, date, duration and any notes about the training session
        user_id (int): User ID for authentication (injected by FastAPI)

    Returns:
        str: Success message indicating the workout report was created

    Raises:
        ForeignKeyViolation: If the referenced workout split does not exist in the database
    """

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
        success_message="Workout Report",
    )


@DATA_POST_API.post("/workout/report/add_set")
async def bind_set_to_report(
    sets: List[schemas.SetReport],
    user_id: int = Depends(TokenService.validate_token),
):
    """
    Add sets to a workout report.

    This endpoint allows users to record the sets performed during a workout session, including details
    like reps completed, weights used, and any notes about the set execution. Multiple sets can be 
    added at once to efficiently track a complete exercise performance.

    Args:
        sets (List[schemas.SetReport]): List of sets to add to the report, containing:
            - split_exercise_id: ID of the exercise in the workout split
            - workout_report_id: ID of the workout report this set belongs to
            - set_order: Order/sequence number of the set
            - reps: Number of repetitions performed
            - weight: Weight used (in kg)
            - notes: Optional notes about the set execution
        user_id (int): User ID for authentication (injected by FastAPI)

    Returns:
        str: Success message indicating the sets were added to the report

    Raises:
        PrimaryKeyViolation: If any set with the same exercise and order already exists in the report
        ForeignKeyViolation: If the referenced split exercise or workout report doesn't exist
    """
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
        success_message="Set Report",
    )

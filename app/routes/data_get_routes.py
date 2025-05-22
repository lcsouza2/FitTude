from typing import Any, List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy import BinaryExpression, and_, select
from sqlalchemy.orm import InstrumentedAttribute, MappedAsDataclass, joinedload

from app.core.authentication import TokenService
from app.core.config import Config
from app.core.connections import db_connection
from app.core.utils import cached_operation
from app.database import db_mapping

DATA_GET_ROUTER = APIRouter(prefix="/api/data", tags=["Data Get Routes"])


async def _execute_select(
    *,
    table_or_columns: MappedAsDataclass | List[InstrumentedAttribute],
    where_clause: Optional[BinaryExpression] = None,
    group_by: Optional[InstrumentedAttribute | List[InstrumentedAttribute]] = None,
    having: Optional[BinaryExpression] = None,
    order_by: Optional[InstrumentedAttribute | List[InstrumentedAttribute]] = None,
    joins: Optional[List[tuple]] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    distinct: bool = False,
    eager_load: Optional[List[InstrumentedAttribute]] = None,
    active_only: bool = True,
) -> List[Any]:
    """
    Execute a flexible SELECT query with various options.

    Args:
        table_or_columns: The main table or list of columns to select from
        where_clause: Optional WHERE conditions
        group_by: Optional GROUP BY column(s)
        order_by: Optional ORDER BY column(s)
        joins: Optional list of (table, condition) tuples for JOINs
        limit: Optional LIMIT value
        offset: Optional OFFSET value
        distinct: Whether to add DISTINCT to the query
        eager_load: Optional list of relationships to eager load
        active_only: Whether to filter only active records

    Returns:
        List of query results
    """

    query = select(table_or_columns)

    if distinct:
        query = query.distinct()

    if where_clause is not None:
        if active_only and hasattr(table_or_columns, "ativo"):
            where_clause = and_(where_clause, table_or_columns.ativo == True)
        query = query.where(where_clause)

    elif active_only and hasattr(table_or_columns, "ativo"):
        query = query.where(table_or_columns.ativo == True)

    if joins:
        for join_table, join_condition in joins:
            query = query.join(join_table, join_condition)

    if eager_load:
        for relationship in eager_load:
            query = query.options(joinedload(relationship))

    if group_by is not None:
        if isinstance(group_by, list):
            query = query.group_by(*group_by)
        else:
            query = query.group_by(group_by)

    if having is not None:
        query = query.having(having)

    if order_by is not None:
        if isinstance(order_by, list):
            query = query.order_by(*order_by)
        else:
            query = query.order_by(order_by)

    if limit is not None:
        query = query.limit(limit)

    if offset is not None:
        query = query.offset(offset)

    async with await db_connection() as session:
        result = await session.scalars(query)
    return result.fetchall()


@cached_operation(Config.CACHE_DEFAULT_TIMEOUT)
async def get_default_muscle_groups() -> list:
    """
    Retrieve default muscle groups from the database.

    Returns:
        list: Default muscle groups (where user_id is None)
    """
    return await _execute_select(
        table_or_columns=db_mapping.MuscleGroup,
        where_clause=db_mapping.MuscleGroup.user_id == None,
    )


@cached_operation(Config.CACHE_DEFAULT_TIMEOUT)
async def get_default_muscles() -> list:
    """
    Retrieve default muscles from the database.

    Returns:
        list: Default muscles (where user_id is None)
    """
    return await _execute_select(
        table_or_columns=db_mapping.Muscle,
        where_clause=db_mapping.Muscle.user_id == None,
    )


@cached_operation(Config.CACHE_DEFAULT_TIMEOUT)
async def get_default_equipment() -> list:
    """
    Retrieve default equipment from the database.

    Returns:
        list: Default equipment (where user_id is None)
    """
    return await _execute_select(
        table_or_columns=db_mapping.Equipment,
        where_clause=db_mapping.Equipment.user_id == None,
    )


@cached_operation(Config.CACHE_DEFAULT_TIMEOUT)
async def get_default_exercises() -> list:
    """
    Retrieve default exercises from the database.

    Returns:
        list: Default exercises (where user_id is None)
    """
    return await _execute_select(
        table_or_columns=db_mapping.Exercise,
        where_clause=db_mapping.Exercise.user_id == None,
    )


@DATA_GET_ROUTER.get("/groups")
async def get_all_muscle_groups(user_id: int = Depends(TokenService.validate_token)):
    """
    Get all muscle groups available to a user.

    Returns both default muscle groups and user-specific ones.
    """
    default_groups = await get_default_muscle_groups()
    user_groups = await _execute_select(
        table_or_columns=db_mapping.MuscleGroup,
        where_clause=db_mapping.MuscleGroup.user_id == user_id,
    )
    return [*default_groups, *user_groups]


@DATA_GET_ROUTER.get("/muscles")
async def get_all_muscles(user_id: int = Depends(TokenService.validate_token)):
    """
    Get all muscles available to a user.

    Returns both default muscles and user-specific ones.
    """
    default_muscles = await get_default_muscles()
    user_muscles = await _execute_select(
        table_or_columns=db_mapping.Muscle,
        where_clause=db_mapping.Muscle.user_id == user_id,
    )
    return [*default_muscles, *user_muscles]


@DATA_GET_ROUTER.get("/equipment")
async def get_all_equipment(user_id: int = Depends(TokenService.validate_token)):
    """
    Get all equipment available to a user.

    Returns both default equipment and user-specific ones.
    """
    default_equipment = await get_default_equipment()
    user_equipment = await _execute_select(
        table_or_columns=db_mapping.Equipment,
        where_clause=db_mapping.Equipment.user_id == user_id,
    )
    return [*default_equipment, *user_equipment]


@DATA_GET_ROUTER.get("/exercises")
async def get_all_exercises(user_id: int = Depends(TokenService.validate_token)):
    """
    Get all exercises available to a user.

    Returns both default exercises and user-specific ones.
    """
    default_exercises = await get_default_exercises()
    user_exercises = await _execute_select(
        table_or_columns=db_mapping.Exercise,
        where_clause=db_mapping.Exercise.user_id == user_id,
    )
    return [*default_exercises, *user_exercises]


@DATA_GET_ROUTER.get("/workout/plans")
async def get_all_workout_plans(user_id: int = Depends(TokenService.validate_token)):
    """
    Get all workout planscreated by user.

    Returns a list of workout plans
    """

    return await _execute_select(
        table_or_columns=db_mapping.WorkoutPlan,
        where_clause=db_mapping.WorkoutPlan.user_id == user_id,
    )


@DATA_GET_ROUTER.get("/workout/splits")
async def get_all_workout_splits(user_id: int = Depends(TokenService.validate_token)):
    """
    Get all workout split created by user.

    Returns a list of workout splits
    """
    return await _execute_select(
        table_or_columns=db_mapping.WorkoutSplit,
        joins=[(db_mapping.WorkoutPlan, None)],
        where_clause=db_mapping.WorkoutPlan.user_id == user_id,
    )


@DATA_GET_ROUTER.get("/workout/split-exercises")
async def get_all_split_exercises(user_id: int = Depends(TokenService.validate_token)):
    """
    Get all exercises bound to a split.

    Returns a list of exercises
    """
    return await _execute_select(
        table_or_columns=db_mapping.SplitExercise,
        joins=[
            (
                db_mapping.WorkoutSplit,
                db_mapping.WorkoutSplit.split == db_mapping.SplitExercise.split,
            ),
            (db_mapping.WorkoutPlan, None),
        ],
        where_clause=db_mapping.WorkoutPlan.user_id == user_id,
    )


@DATA_GET_ROUTER.get("/workout/reports")
async def get_all_workout_reports(user_id: int = Depends(TokenService.validate_token)):
    """
    Get all user workout reports.

    Returns a list of reports
    """
    return await _execute_select(
        table_or_columns=db_mapping.WorkoutReport,
        joins=[(db_mapping.WorkoutPlan, None)],
        where_clause=db_mapping.WorkoutPlan.user_id == user_id,
    )

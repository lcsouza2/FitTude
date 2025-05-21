from typing import Any, List, Optional, Union

from fastapi import APIRouter, Depends
from sqlalchemy import BinaryExpression, and_, or_, select
from sqlalchemy.orm import InstrumentedAttribute, MappedAsDataclass, joinedload

from app.core.authentication import TokenService
from app.core.connections import db_connection
from app.core.utils import cached_operation

from app.database import db_mapping

DATA_GET_API = APIRouter(prefix="/api/data", tags=["Data Get Routes"])


async def _execute_select(
    *,
    table_or_columns: MappedAsDataclass | List[InstrumentedAttribute],
    where_clause: Optional[BinaryExpression] = None,
    group_by: Optional[
        Union[InstrumentedAttribute, List[InstrumentedAttribute]]
    ] = None,
    having: Optional[BinaryExpression] = None,
    order_by: Optional[
        Union[InstrumentedAttribute, List[InstrumentedAttribute]]
    ] = None,
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
    # Start building the query
    query = select(table_or_columns)

    if distinct:
        query = query.distinct()

    # Add WHERE clause if provided
    if where_clause is not None:
        if active_only and hasattr(table_or_columns, "ativo"):
            where_clause = and_(where_clause, table_or_columns.ativo == True)
        query = query.where(where_clause)
    elif active_only and hasattr(table_or_columns, "ativo"):
        query = query.where(table_or_columns.ativo == True)

    # Add JOINs if provided
    if joins:
        for join_table, join_condition in joins:
            query = query.join(join_table, join_condition)

    # Add eager loading if provided
    if eager_load:
        for relationship in eager_load:
            query = query.options(joinedload(relationship))

    # Add GROUP BY if provided
    if group_by is not None:
        if isinstance(group_by, list):
            query = query.group_by(*group_by)
        else:
            query = query.group_by(group_by)

    # Add HAVING if provided
    if having is not None:
        query = query.having(having)

    # Add ORDER BY if provided
    if order_by is not None:
        if isinstance(order_by, list):
            query = query.order_by(*order_by)
        else:
            query = query.order_by(order_by)

    # Add LIMIT and OFFSET if provided
    if limit is not None:
        query = query.limit(limit)
    if offset is not None:
        query = query.offset(offset)

    async with await db_connection() as session:
        # Execute the query
        result = await session.scalars(query)
    return result.fetchall()


@DATA_GET_API.get("/groups")
@cached_operation(timeout=3600)
async def get_all_muscle_groups(user_id: int = Depends(TokenService.validate_token)):
    return await _execute_select(
        table_or_columns=db_mapping.MuscleGroup,
        where_clause=or_(
            db_mapping.MuscleGroup.user_id == user_id,
            db_mapping.MuscleGroup.user_id == None,
        ),
    )


@DATA_GET_API.get("/muscles")
@cached_operation(timeout=3600)
async def get_all_muscles(user_id: int = Depends(TokenService.validate_token)):
    return await _execute_select(
        table_or_columns=db_mapping.Muscle,
        where_clause=or_(
            db_mapping.Muscle.user_id == user_id,
            db_mapping.Muscle.user_id == None,
        ),
    )


@DATA_GET_API.get("/equipment")
@cached_operation(timeout=3600)
async def get_all_equipment(user_id: int = Depends(TokenService.validate_token)):
    return await _execute_select(
        table_or_columns=db_mapping.Equipment,
        where_clause=or_(
            db_mapping.Equipment.user_id == user_id,
            db_mapping.Equipment.user_id == None,
        ),
    )


@DATA_GET_API.get("/exercises")
async def get_all_exercises(user_id: int = Depends(TokenService.validate_token)):
    return await _execute_select(
        table_or_columns=db_mapping.Exercise,
        where_clause=or_(
            db_mapping.Exercise.user_id == user_id,
            db_mapping.Exercise.user_id == None,
        ),
    )


@DATA_GET_API.get("/workout/plans")
async def get_all_workout_plans(user_id: int = Depends(TokenService.validate_token)):
    return await _execute_select(
        table_or_columns=db_mapping.WorkoutPlan,
        where_clause=db_mapping.WorkoutPlan.user_id == user_id,
    )


@DATA_GET_API.get("/workout/splits")
async def get_all_workout_splits(user_id: int = Depends(TokenService.validate_token)):
    return await _execute_select(
        table_or_columns=db_mapping.WorkoutSplit,
        joins=[(db_mapping.WorkoutPlan, None)],
        where_clause=db_mapping.WorkoutPlan.user_id == user_id,
    )


@DATA_GET_API.get("/workout/split-exercises")
async def get_all_split_exercises(user_id: int = Depends(TokenService.validate_token)):
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


@DATA_GET_API.get("/workout/reports")
async def get_all_workout_reports(user_id: int = Depends(TokenService.validate_token)):
    return await _execute_select(
        table_or_columns=db_mapping.WorkoutReport,
        joins=[(db_mapping.WorkoutPlan, None)],
        where_clause=db_mapping.WorkoutPlan.user_id == user_id,
    )

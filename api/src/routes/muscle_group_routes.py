from fastapi import APIRouter, Depends, status
from src.connections import AsyncSessionInjector, RedisInjector
from src.repository.muscle_group_repository import MuscleGroupRepository
from src.services.muscle_group_service import MuscleGroupService
from src.schemas.muscle_group_schemas import (
    MuscleGroupCreateSchema,
    MuscleGroupUpdateSchema,
    MuscleGroupResponseSchema,
)
router = APIRouter(prefix="/groups", tags=["Muscle Groups"])

class _RequestDeps:
    def __init__(self, session: AsyncSessionInjector, redis: RedisInjector):
        self.session = session
        self.redis = redis
        self.service = MuscleGroupService(self.session)

@router.get("/", response_model=list[MuscleGroupResponseSchema])
async def get_all_muscle_groups(
    deps: _RequestDeps = Depends(),
):
    return await deps.service.get_all_muscle_groups()

@router.get("/{group_name}", response_model=MuscleGroupResponseSchema)
async def get_muscle_group_by_name(
    group_name: str,
    user_id: int,
    deps: _RequestDeps = Depends(),
):
    return await deps.service.get_muscle_group_by_name(group_name, user_id)

@router.post("/", response_model=MuscleGroupResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_muscle_group(
    muscle_group: MuscleGroupCreateSchema,
    deps: _RequestDeps = Depends(),
):
    return await deps.service.create_muscle_group(muscle_group)
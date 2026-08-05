from src.schemas.muscle_group_schemas import MuscleGroupCreateSchema, MuscleGroupUpdateSchema, MuscleGroupResponseSchema
from src.repository.muscle_group_repository import MuscleGroupRepository
from sqlalchemy.ext.asyncio import AsyncSession

class MuscleGroupService:
    def __init__(self, session: AsyncSession):
        self.repo = MuscleGroupRepository(session)

    async def get_all_muscle_groups(self):
        return await self.repo.get_all_muscle_groups()

    async def get_muscle_group_by_name(self, group_name: str, user_id: int):
        return await self.repo.get_muscle_group_by_name(group_name, user_id)

    async def create_muscle_group(self, data: MuscleGroupCreateSchema):
        data_as_dict = data.model_dump()
        return await self.repo.create_muscle_group(data_as_dict)


    async def update_muscle_group(self, group_name: str, user_id: int, data: MuscleGroupUpdateSchema):
        data_as_dict = data.model_dump()
        return await self.repo.update_muscle_group(group_name, user_id, data_as_dict)

    async def delete_muscle_group(self, group_name: str, user_id: int):
        return await self.repo.delete_muscle_group(group_name, user_id)


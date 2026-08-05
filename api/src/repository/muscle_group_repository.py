from datetime import datetime
from src.models import MuscleGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update

class MuscleGroupRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_muscle_groups(self):
        result = await self.db.execute(select(MuscleGroup).where(MuscleGroup.deleted == False))
        return result.scalars().all()

    async def create_muscle_group(self, data: dict):
        result = await self.db.execute(insert(MuscleGroup).values(**data).returning(MuscleGroup))
        return result.scalar_one_or_none()

    async def get_muscle_group_by_name(self, group_name: str, user_id: int):
        result = await self.db.execute(
            select(MuscleGroup).where(MuscleGroup.group_name == group_name, MuscleGroup.user_id == user_id, MuscleGroup.deleted == False)
        )
        return result.scalar_one_or_none()

    async def update_muscle_group(self, group_name: str, user_id: int, data: dict):
        query = (
            update(MuscleGroup)
            .where(MuscleGroup.group_name == group_name, MuscleGroup.user_id == user_id, MuscleGroup.deleted == False)
            .values(**data)
            .returning(MuscleGroup)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def delete_muscle_group(self, group_name: str, user_id: int):
        query = (
            update(MuscleGroup)
            .where(MuscleGroup.group_name == group_name, MuscleGroup.user_id == user_id, MuscleGroup.deleted == False)
            .values(deleted=True, deleted_at=datetime.now())
            .returning(MuscleGroup)
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
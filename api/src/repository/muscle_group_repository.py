from ast import stmt

from api.src.models import MuscleGroup
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

class MuscleGroupRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_muscle_groups(self):
        result = await self.db.execute(select(MuscleGroup))
        return result.scalars().all()

    async def create_muscle_group(self, data: dict):
        result = await self.db.execute(insert(MuscleGroup).values(**data).returning(MuscleGroup))
        await self.db.commit()
        return result.one_or_none()
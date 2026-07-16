from api.src.models import Muscle
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, select

class MuscleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_muscle_by_id(self, muscle_id):
        query = select(Muscle).where(Muscle.id == muscle_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_all_muscles(self):
        query = select(Muscle)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_muscle(self, data: dict):
        result = await self.db.execute(insert(Muscle).values(data).returning(Muscle))
        return result.scalar_one_or_none()
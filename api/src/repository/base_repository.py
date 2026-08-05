from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def paginate_mapping(self, query, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        result = await self.session.execute(select(query).select_from(query).offset(offset).limit(page_size))
        result = result.scalars().all()

        return result
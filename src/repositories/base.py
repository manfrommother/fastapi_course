from sqlalchemy import select, insert


class BaseRepository:
    model = None
    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filtered_by):
        query = select(self.model).filter_by(**filtered_by)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add(self, data: dict):
        stm_add = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stm_add)
        await self.session.flush()
        return result.scalar_one()



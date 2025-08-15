from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel


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

    async def add(self, data: BaseModel):
        stm_add = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stm_add)
        return result.scalars().one()

    async def edit(self, data: BaseModel, **filtered_by):
        count_stm = select(self.model).filter_by(**filtered_by)
        result = await self.session.execute(count_stm)
        matches = result.scalars().all()
        if not matches:
            raise HTTPException(status_code=404)
        if len(matches) > 1:
            raise HTTPException(status_code=422)
        query = (
            update(self.model)
            .filter_by(**filtered_by)
            .values(**data.model_dump())
        )
        await self.session.execute(query)

    async def delete(self, **filtered_by):
        count_stm = select(self.model).filter_by(**filtered_by)
        result = await self.session.execute(count_stm)
        matches = result.scalars().all()
        if not matches:
            raise HTTPException(status_code=404)
        if len(matches) > 1:
            raise HTTPException(status_code=422)
        query = (
            delete(self.model)
            .filter_by(**filtered_by)
        )
        await self.session.execute(query)

from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel

from src.schemas.hotels import Hotel


class BaseRepository:
    model = None
    schema: BaseModel = None


    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]


    async def get_one_or_none(self, **filtered_by):
        query = select(self.model).filter_by(**filtered_by)
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model)

    async def add(self, data: BaseModel):
        stm_add = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stm_add)
        model = result.scalars().one()
        return self.schema.model_validate(model)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filtered_by):
        update_stmt = (
            update(self.model)
            .filter_by(**filtered_by)
            .values(**data
                    .model_dump(exclude_unset=exclude_unset))
        )
        await self.session.execute(update_stmt)

    async def delete(self, **filtered_by):
        delete_stmt = delete(self.model).filter_by(**filtered_by)
        await self.session.execute(delete_stmt)

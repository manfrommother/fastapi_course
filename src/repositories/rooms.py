from pydantic import BaseModel
from sqlalchemy import select, insert, update, delete

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.schemas.rooms import Rooms


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Rooms

    async def get_rooms_by_hotel(self, hotel_id: int):
        query = select(RoomsOrm).where(RoomsOrm.hotel_id==hotel_id)
        result = await self.session.execute(query)
        return [Rooms.model_validate(model) for model in result.scalars().all()]

    async def add_room(self, hotel_id: int, model: BaseModel):
        query  = insert(RoomsOrm).values(hotel_id=hotel_id, **model.model_dump()).returning(RoomsOrm)
        result = await self.session.execute(query)
        return result.scalars().one()

    async def delete_room(self, room_id: int):
        query = delete(RoomsOrm).where(RoomsOrm.id==room_id)
        await self.session.execute(query)


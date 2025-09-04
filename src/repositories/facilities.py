from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.repositories.mappers.mappers import FacilitiesDataMapper
from src.schemas.facilities import Facilities, RoomsFacility
from src.repositories.base import BaseRepository

from sqlalchemy import select, delete, insert


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    mapper = FacilitiesDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomsFacility

    async def set_room_facilities(self, room_id: int, facilities_ids: list[int]):
        get_current_facilities_ids_query = (
            select(self.model.facility_id).
            filter_by(rooms_id=room_id)
        )
        res = await self.session.execute(get_current_facilities_ids_query)
        current_facilities_ids = res.scalars().all()
        ids_to_delete = list(set(current_facilities_ids) - set(facilities_ids))
        ids_to_insert = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:
            delete_m2m_facilities_stmt = (
                delete(self.model)
                .filter(
                    self.model.rooms_id == room_id,
                    self.model.facility_id.in_(ids_to_delete))
            )
            await self.session.execute(delete_m2m_facilities_stmt)

        if ids_to_insert:
            insert_m2m_facilities_stmt = (
                insert(self.model)
                .values([{"rooms_id": room_id, "facility_id": f_id} for f_id in ids_to_insert])
            )
            await self.session.execute(insert_m2m_facilities_stmt)
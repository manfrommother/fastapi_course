from datetime import date

from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomsFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])

@router.get("/{hotel_id}/rooms")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date,
        date_to: date,
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post("/{hotel_id}/rooms")
async def create_rooms(hotel_id: int, db: DBDep, room_data: RoomAddRequest = Body()):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    if room_data.facilities_ids:
        rooms_facilities_data = [RoomsFacilityAdd(rooms_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
        await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "result": room}

@router.delete("{hotel_id}/rooms/{room_id}")
async def delete_rooms(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()

    return {"status": "OK"}

@router.put("/{hotel_id}/rooms/{room_id}")
async def edit_rooms(hotel_id: int, room_id: int, room_data: RoomAddRequest, db: DBDep):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id)
    # Обновление удобств комнаты (дифф)
    if room_data.facilities_ids is not None:
        existing = await db.rooms_facilities.get_filtered(rooms_id=room_id)
        existing_ids = {item.facility_id for item in existing}
        new_ids = set(room_data.facilities_ids)

        to_add = new_ids - existing_ids
        to_remove = existing_ids - new_ids

        if to_add:
            add_payload = [RoomsFacilityAdd(rooms_id=room_id, facility_id=fid) for fid in to_add]
            await db.rooms_facilities.add_bulk(add_payload)
        if to_remove:
            for fid in to_remove:
                await db.rooms_facilities.delete(rooms_id=room_id, facility_id=fid)
    await db.commit()

    return {"status": "OK"}

@router.patch("{hotel_id}/rooms/{room_id}")
async def partially_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
        db: DBDep
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, exclude_unset=True ,id=room_id, hotel_id=hotel_id)
    # Обновление удобств комнаты (дифф), только если поле передано
    if room_data.facilities_ids is not None:
        existing = await db.rooms_facilities.get_filtered(rooms_id=room_id)
        existing_ids = {item.facility_id for item in existing}
        new_ids = set(room_data.facilities_ids)

        to_add = new_ids - existing_ids
        to_remove = existing_ids - new_ids

        if to_add:
            add_payload = [RoomsFacilityAdd(rooms_id=room_id, facility_id=fid) for fid in to_add]
            await db.rooms_facilities.add_bulk(add_payload)
        if to_remove:
            for fid in to_remove:
                await db.rooms_facilities.delete(rooms_id=room_id, facility_id=fid)
    await db.commit()

    return {"status": "OK"}
from fastapi import APIRouter, Body
from pydantic import BaseModel

from src.repositories.rooms import RoomsRepository
from src.database import async_session_maker
from src.schemas.rooms import RoomsAdd, RoomsPatch

router = APIRouter(prefix="/hotels", tags=["Номера отелей"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_rooms_by_hotel(hotel_id)


@router.post("/{hotel_id}/rooms")
async def add_rooms(hotel_id: int, rooms_model: RoomsAdd = Body()):
    async with async_session_maker() as session:
        result = await RoomsRepository(session).add_room(hotel_id, rooms_model)
        await session.commit()

    return {"status": "OK", "result": result}

@router.delete("/rooms/{room_id}")
async def delete_rooms(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete_room(room_id)
        await session.commit()

    return {"status": "OK"}

@router.put("/rooms/{room_id}")
async def update_rooms(room_id: int, rooms_model: RoomsAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(rooms_model, id=room_id)
        await session.commit()
    return {"status": "OK"}

@router.patch("/rooms/{room_id}")
async def edit_rooms(room_id: int, rooms_data: RoomsPatch):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(rooms_data, exclude_unset=True ,id=room_id)
        await session.commit()

    return {"status": "OK"}
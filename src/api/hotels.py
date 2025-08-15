from fastapi import Query, Body, APIRouter

from sqlalchemy import insert, select

from src.database import async_session_maker
from src.models.hotels import HotelsOrm
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels")


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        location: str | None = Query(None, description="Адрес"),
        title: str | None= Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )



@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1":{"summary": "Сочи", "value": {
        "title": "Отел Сочи 5* у моря",
        "location": "Сочи у моря",
    }},
    "2":{"summary": "Дубайск", "value": {
        "title": "Отел Дубайск 5* у моря",
        "location": "Дубайск у моря",
    }},
})):
    async with async_session_maker() as session:
        repo = HotelsRepository(session)
        hotel = await repo.add(hotel_data.model_dump())
        await session.commit()

    return {"status": "OK", "data": hotel}

@router.put("/{hotel_id}")
def update_hotel_info(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name

    return {"status": "OK"}

@router.patch("/{hotel_id}")
def update_hotel_info(hotel_id: int, hotel_data: HotelPatch):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}

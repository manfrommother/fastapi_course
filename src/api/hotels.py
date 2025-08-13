from fastapi import Query, Body, APIRouter

from src.schemas.hotels import Hotel, HotelPatch
from src.api.dependencies import PaginationDep

router = APIRouter(prefix="/hotels")
hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

@router.get("")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None= Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]
    return hotels_

@router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}

@router.post("")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1":{"summary": "Сочи", "value": {
        "title": "Отел Сочи 5* у моря",
        "name": "Сочи у моря",
    }},
    "2":{"summary": "Дубайск", "value": {
        "title": "Отел Дубайск 5* у моря",
        "name": "Дубайск у моря",
    }},
})):
    global hotels
    hotels.append({"id": hotels[-1]["id"] + 1,
                   "title": hotel_data.title,
                    "name": hotel_data.name}),
    return {"status": "OK"}

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

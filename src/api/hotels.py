from fastapi import Query, Body, APIRouter

from src.database import async_session_maker
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPatch, HotelAdd
from src.api.dependencies import PaginationDep, DBDep

router = APIRouter(prefix="/hotels", tags=["hotels"])


@router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        location: str | None = Query(None, description="Адрес"),
        title: str | None= Query(None, description="Название отеля"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )

@router.get("/{hotel_id}")
async def get_hotel_by_id(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"status": "OK"}

@router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    "1":{"summary": "Сочи", "value": {
        "title": "Отел Сочи 5* у моря",
        "location": "Сочи у моря",
    }},
    "2":{"summary": "Дубайск", "value": {
        "title": "Отел Дубайск 5* у моря",
        "location": "Дубайск у моря",
    }},
})):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}

@router.put("/{hotel_id}")
async def edit_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()

    return {"status": "OK"}

@router.patch("/{hotel_id}")
async def partially_edit_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}

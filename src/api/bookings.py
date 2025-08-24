from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.models.bookings import BookingsOrm
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def create_booking(
        db: DBDep,
        booking_data: BookingAddRequest,
        user_id: UserIdDep):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room.price,
        **booking_data.model_dump()
    )
    result = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": result}


@router.get("")
async def get_all_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get("/me")
async def get_users_bookings(db: DBDep, user_id: UserIdDep):
    return await db.bookings.get_filtered(user_id=user_id)


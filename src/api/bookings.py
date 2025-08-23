from fastapi import APIRouter

from src.api.dependencies import DBDep, UserIdDep
from src.models.bookings import BookingsOrm
from src.schemas.bookings import BookingRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.post("")
async def create_booking(
        db: DBDep,
        booking_data: BookingRequest,
        user_id: UserIdDep):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    _booking_data = BookingAdd(user_id=user_id, price=room.price, **booking_data.model_dump())
    result = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "result": result}


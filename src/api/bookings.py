from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd


router = APIRouter(prefix="/bookings", tags=["Бронирования"])


@router.get(
    "",
    summary="Получение информации о всех бронированиях",
    description="<h1>Получение информации всех существующих бронирований</h1>"
)
async def get_bookings(db: DBDep):
    return await db.bookings.get_all()


@router.get(
    "/me",
    summary="Получение информации о бронированиях одного пользователя",
    description="<h1>Получение информации о всех бронированиях пользователя только если он аутентифицирован</h1>"
)
async def get_my_bookings(user_id: UserIdDep, db: DBDep):
    return await db.bookings.get_filtered(user_id=user_id)


@router.post(
    "",
    summary="Создание нового бронирования",
    description="<h1>Создание нового бронированиях для аутентифицированного пользователя</h1>"
)
async def add_booking(
        user_id: UserIdDep,
        db: DBDep,
        booking_data: BookingAddRequest = Body(openapi_examples={
    "1": {"summary": "test_1", "value":{
        "room_id": 8,
        "date_from": "2026-02-15",
        "date_to": "2026-03-15",
    }},
    "2": {"summary": "test_2", "value":{
        "title": 21,
        "date_from": "2026-02-15",
        "date_to": "2026-03-15",
    }},
})
):
    room = await db.rooms.get_one_or_none(id=booking_data.room_id)
    room_price = room.price
    _booking_data = BookingAdd(
        user_id=user_id,
        price=room_price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
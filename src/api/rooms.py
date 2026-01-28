from datetime import date

from fastapi import APIRouter, Path, Body, Query

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomPatchRequest, RoomAddRequest

router = APIRouter(prefix="/hotel/{hotel_id}", tags=["Номера"])


@router.get(
    "/rooms",
    summary="Получение всех данных",
    description="<h1>Тут мы получаем все номера одного отеля</h1>",
)
async def get_rooms(
        db: DBDep,
        hotel_id: int = Path(description="Уникальный идентификатор отеля"),
        date_from: date = Query(example="2026-01-24", description="Дата заезда"),
        date_to: date = Query(example="2026-01-31", description="Дата выезда"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get(
    "/rooms/{room_id}",
    summary="Получение информации одного номера",
    description="<h1>Получении информации одного конкретного номера в отеле по их id</h1>",
)
async def get_particular_rooms(
        db: DBDep,
        hotel_id: int = Path(description="Уникальный идентификатор отеля"),
        room_id: int = Path(description="Уникальный идентификатор номера")
):
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post(
    "/rooms",
    summary="Добавление новых данных",
    description="<h1>Добавление информации о новом номере в отеле</h1>",
)
async def create_room(
        db: DBDep,
        hotel_id: int = Path(description="Уникальный идентификатор отеля"),
        room_data: RoomAddRequest = Body(openapi_examples={
    "1": {"summary": "test_1", "value":{
        "title": "Luxe",
        "description": "Большой номер со всеми удобствами",
        "price": "10000",
        "quantity": "1",
        "facilities_ids": [1]
    }},
    "2": {"summary": "test_2", "value":{
        "title": "Односпальный",
        "price": "1500",
        "quantity": "4",
        "facilities_ids": [2]
    }},
})
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]

    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put(
    "/rooms/{room_id}",
    summary="Полное обновление данных",
    description="<h1>Позволяет полностью обновить все данные о номере</h1>",
)
async def edit_room(
        db: DBDep,
        room_data: RoomAddRequest,
        hotel_id: int = Path(description="Уникальный идентификатор отеля"),
        room_id: int = Path(description="Уникальный идентификатор номера")
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(id=room_id, data=_room_data, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch(
    "/rooms/{room_id}",
    summary="Частичное обновление данных",
    description="<h1>Позволяет частично обновить данные о номере</h1>",
)
async def partially_edit_hotel(
        db: DBDep,
        room_data: RoomPatchRequest,
        hotel_id: int = Path(description="Уникальный идентификатор отеля"),
        room_id: int = Path(description="Уникальный идентификатор номера")
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(
        hotel_id=hotel_id,
        id=room_id,
        exclude_unset=True,
        data=_room_data
    )
    await db.commit()
    return {"status": "OK"}


@router.delete(
    "/rooms/{room_id}",
    summary="Полное удаление данных",
    description="<h1>ОСТОРОЖНО! Позволяет полностью удалить все данные о номере</h1>",
)
async def delete_room(
        db: DBDep,
        hotel_id: int = Path(description="Уникальный идентификатор отеля"),
        room_id: int = Path(description="Уникальный идентификатор номера")
):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}
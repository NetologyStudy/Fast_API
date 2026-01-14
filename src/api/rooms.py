from fastapi import APIRouter, Path, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPatch, RoomPatchRequest, RoomAddRequest

router = APIRouter(prefix="/hotel/{hotel_id}", tags=["Номера"])


@router.get(
    "/rooms",
    summary="Получение всех данных",
    description="<h1>Тут мы получаем все номера одного отеля</h1>",
)
async def get_rooms(hotel_id: int = Path(description="Уникальный идентификатор отеля")):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_filtered(hotel_id=hotel_id)


@router.get(
    "/rooms/{room_id}",
    summary="Получение информации одного номера",
    description="<h1>Получении информации одного конкретного номера в отеле по их id</h1>",
)
async def get_particular_rooms(
        hotel_id: int = Path(description="Уникальный идентификатор отеля"),
        room_id: int = Path(description="Уникальный идентификатор номера")
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id, hotel_id=hotel_id)


@router.post(
    "/rooms",
    summary="Добавление новых данных",
    description="<h1>Добавление информации о новом номере в отеле</h1>",
)
async def create_room(
        room_data: RoomAddRequest,
        hotel_id: int = Path(description="Уникальный идентификатор отеля"),
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(_room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put(
    "/rooms/{room_id}",
    summary="Полное обновление данных",
    description="<h1>Позволяет полностью обновить все данные о номере</h1>",
)
async def edit_room(
        room_data: RoomAddRequest,
        hotel_id: int = Path(description="Уникальный идентификатор отеля"),
        room_id: int = Path(description="Уникальный идентификатор номера")
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(id=room_id, data=_room_data, hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch(
    "/rooms/{room_id}",
    summary="Частичное обновление данных",
    description="<h1>Позволяет частично обновить данные о номере</h1>",
)
async def partially_edit_hotel(
        room_data: RoomPatchRequest,
        hotel_id: int = Path(description="Уникальный идентификатор отеля"),
        room_id: int = Path(description="Уникальный идентификатор номера")
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(
            hotel_id=hotel_id,
            id=room_id,
            exclude_unset=True,
            data=_room_data
        )
        await session.commit()
    return {"status": "OK"}


@router.delete(
    "/rooms/{room_id}",
    summary="Полное удаление данных",
    description="<h1>ОСТОРОЖНО! Позволяет полностью удалить все данные о номере</h1>",
)
async def delete_room(
        hotel_id: int = Path(description="Уникальный идентификатор отеля"),
        room_id: int = Path(description="Уникальный идентификатор номера")
):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}
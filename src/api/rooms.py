from fastapi import APIRouter, Path, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPATCH

router = APIRouter(prefix="/hotel/{hotel_id}", tags=["Номера"])


@router.get("")
async def get_rooms():
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all()


@router.get("/rooms/{room_id}")
async def get_particular_rooms(room_id: int = Path(description="Уникальный идентификатор")):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(id=room_id)


@router.post("/rooms")
async def create_room(room_data: RoomAdd):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/rooms")
async def edit_room(room_data: RoomAdd, room_id: int = Path()):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(id=room_id, data=room_data)
        await session.commit()
    return {"status": "OK"}


@router.patch("/rooms")
async def partially_edit_hotel(room_data: RoomPATCH, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(id=room_id, exclude_unset=True, data=room_data)
        await session.commit()
    return {"status": "OK"}


@router.delete("/rooms")
async def delete_room(room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id)
        await session.commit()
    return {"status": "OK"}
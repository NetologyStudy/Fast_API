from datetime import date

from fastapi import Query, Path, APIRouter, Body

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPatch, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get(
    "",
    summary="Получение всех данных",
    description="<h1>Позволяет получить полную информацию о всех отелях</h1>"
)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название"),
        location: str | None = Query(None, description="Месторпасположение"),
        stars: int | None = Query(None, description="Количество звезд"),
        date_from: date = Query(example="2026-01-24", description="Дата заезда"),
        date_to: date = Query(example="2026-01-31", description="Дата выезда"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        location=location,
        title=title,
        stars=stars,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get(
    "/{hotel_id}",
    summary="Получение информации одного отеля",
    description="<h1>Получение информации одного конкретного отеля по его id</h1>"
)
async def get_one_hotels(db: DBDep, hotel_id: int = Path(description="Уникальный идентификатор")):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post(
    "",
    summary="Добавлениие новых данных",
    description="<h1>Добавление полностью новой информации: нового отеля и его данных</h1>"
)
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    "1": {"summary": "Сочи", "value":{
        "title": "Отель Rich у моря",
        "location": "Sochi, Russia",
        "stars": "4",
    }},
    "2": {"summary": "Дубай", "value":{
        "title": "Отель RELAX у фонтана",
        "location": "Dubai, UAE",
        "stars": "5",
    }},
})
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()

    return {"status": "OK", "data": hotel}


@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных",
    description="<h1>Позволяет обновить всю информациию выбранного отеля</h1>"
)
async def edit_hotel(
        db: DBDep,
        hotel_data: HotelAdd,
        hotel_id: int = Path(description="Уникальный идентификатор")
):
    await db.hotels.edit(id=hotel_id, data=hotel_data)
    await db.commit()

    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных",
    description="<h1>Позволяет частично обновить инофрмацию выбранного отеля</h1>"
)
async def partially_edit_hotel(
        db: DBDep,
        hotel_data: HotelPatch,
        hotel_id: int = Path(description="Уникальный идентификатор")
):
    await db.hotels.edit(id=hotel_id, exclude_unset=True, data=hotel_data)
    await db.commit()
    return {"status": "OK"}

@router.delete(
    "/{hotel_id}",
    summary="Полное удаление данных",
    description="<h1>ОСТОРОЖНО! Полностью удаляет всю информацию выбранного отеля!</h1>"
)
async def delete_hotel(db: DBDep, hotel_id: int = Path(description="Уникальный идентификатор")):
    await db.hotels.delete(id=hotel_id)
    await db.commit()

    return {"status": "OK"}

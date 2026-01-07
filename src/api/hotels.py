from fastapi import Query, Path, APIRouter, Body

from sqlalchemy import insert, select

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отили"])


@router.get(
    "",
    summary="Получение всех данных",
    description="<h1>Позволяет получить полную информацию о всех отелях</h1>"
)
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название"),
        location: str | None = Query(None, description="Месторпасположение"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.icontains(location.strip()))
        if title:
            query = query.filter(HotelsOrm.title.icontains(title.strip()))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )
        print(query.compile(compile_kwargs={"literal_binds": True}))
        result = await session.execute(query)
        hotels = result.scalars().all()
        return hotels


@router.post(
    "",
    summary="Добавлениие новых данных",
    description="<h1>Добавление полностью новой информации: нового отеля и его данных</h1>"
)
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value":{
        "title": "Отель Rich 5 звезд у моря",
        "location": "Sochi, Russia",
    }},
    "2": {"summary": "Дубай", "value":{
        "title": "Отель RELAX 5 звезд у моря",
        "location": "Dubai, UAE",
    }},
})
):
    async with async_session_maker() as session:
        add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()

    return {"status": "OK"}


@router.put(
    "/{hotel_id}",
    summary="Полное обновление данных",
    description="<h1>Позволяет обновить всю информациию выбранного отеля</h1>"
)
def edit_hotel(
        hotel_data: Hotel,
        hotel_id: int = Path(description="Уникальный идентификатор")
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_id == hotel["id"]:
        hotel["title"] = hotel_data.title
        hotel["location"] = hotel_data.location
    return {"status": "OK"}


@router.patch(
    "/{hotel_id}",
    summary="Частичное обновление данных",
    description="<h1>Позволяет частично обновить инофрмацию выбранного отеля</h1>"
)
def partially_edit_hotel(
        hotel_data: HotelPATCH,
        hotel_id: int = Path(description="Уникальный идентификатор")
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if  hotel_data.location:
        hotel["location"] = hotel_data.location
    return {"status": "OK"}

@router.delete(
    "/{hotel_id}",
    summary="Полное удаление данных",
    description="<h1>ОСТОРОЖНО! Полностью удаляет всю информацию выбранного отеля!</h1>"
)
def delete_hotel(hotel_id: int = Path(description="Уникальный идентификатор")):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}
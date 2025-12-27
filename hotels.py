from fastapi import Query, Path, APIRouter, Body

from dependencies import PaginationDep
from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отили"])


hotels = [
    {"id": 1, "title": "Сочи", "location": "sochi"},
    {"id": 2, "title": "Дубай", "location": "dubai"},
    {"id": 3, "title": "Москва", "location": "moscva"},
    {"id": 4, "title": "Калининград", "location": "kaliningrad"},
    {"id": 5, "title": "Питер", "location": "spb"},
    {"id": 6, "title": "Вологда", "location": "vologda"},
    {"id": 7, "title": "Череповец", "location": "che"},
]


@router.get(
    "",
    summary="Получение всех данных",
    description="<h1>Позволяет получить полную информацию о всех отелях</h1>"
)
def get_hotels(
        pagination: PaginationDep,
        id: int | None= Query(None, description="Уникальный идентификатор"),
        title: str | None = Query(None, description="Название"),
        location: str | None = Query(None, description="Местонахождение"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        if location and hotel["location"] != location:
            continue
        hotels_.append(hotel)
    return hotels_[pagination.per_page * (pagination.page - 1):][:pagination.per_page]



@router.post(
    "",
    summary="Добавлениие новых данных",
    description="<h1>Добавление полностью новой информации: нового отеля и его данных</h1>"
)
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Сочи", "value":{
        "title": "Сочи 5 звезд у моря",
        "location": "Sochi, Russia",
    }},
    "2": {"summary": "Дубай", "value":{
        "title": "Дубай 5 звезд у моря",
        "location": "Dubai, UAE",
    }},
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
         "title": hotel_data.title,
         "location": hotel_data.location,
    })
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
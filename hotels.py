from fastapi import Query, Path, APIRouter

from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отили"])


hotels = [
    {"id": 1, "title": "Sochi", "location": "sochi"},
    {"id": 2, "title": "Дубай", "location": "дубай"}
]


@router.get(
    "",
    summary="Получение всех данных",
    description="<h1>Позволяет получить полную информацию о всех отелях</h1>"
)
def get_hotels(
        id: int | None= Query(None, description="Уникальный идентификатор"),
        title: str | None = Query(None, description="Название"),
        location: str | None = Query(None, description="Местонахождение")
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
    return hotels_


@router.post(
    "",
    summary="Добавлениие новых данных",
    description="<h1>Добавление полностью новой информации: нового отеля и его данных</h1>"
)
def create_hotel(hotel_data: Hotel):
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
        hotel_data: HotelsPATCH,
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
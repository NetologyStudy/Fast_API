import uvicorn
from fastapi import FastAPI, Query, Body, Path


app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi", "location": "sochi"},
    {"id": 2, "title": "Дубай", "location": "дубай"}
]


@app.get(
    "/hotels",
    summary="Получение всех данных",
    description="<h1>Позволяет получить полную информацию о всех отелях</h1>"
)
def get_hotels(
        id: int | None= Query(None, description="Уникальный идентификатор"),
        title: str | None = Query(None, description="Название"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.post(
    "/hotels",
    summary="Добавлениие новых данных",
    description="<h1>Добавление полностью новой информации: нового отеля и его данных</h1>"
)
def create_hotel(
        title: str =  Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
         "title": title,
    })
    return {"status": "OK"}


@app.put(
    "/hotels/{hotel_id}",
    summary="Полное обновление данных",
    description="<h1>Позволяет обновить всю информациию выбранного отеля</h1>"
)
def edit_hotel(
        hotel_id: int = Path(description="Уникальный идентификатор"),
        title: str = Body(description="Название"),
        location: str = Body(description="Местонахождение"),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_id == hotel["id"]:
        hotel["title"] = title
        hotel["location"] = location
    return {"status": "OK"}


@app.patch(
    "/hotels/{hotel_id}",
    summary="Частичное обновление данных",
    description="<h1>Позволяет частично обновить инофрмацию выбранного отеля</h1>"
)
def partially_edit_hotel(
        hotel_id: int = Path(description="Уникальный идентификатор"),
        title: str | None = Body(None, description="Название"),
        location: str | None = Body(None, description="Местонахождение"),
):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_id == hotel["id"]:
        hotel["title"] = title
        hotel["location"] = location
    return {"status": "OK"}

@app.delete(
    "/hotels/{hotel_id}",
    summary="Полное удаление данных",
    description="<h1>ОСТОРОЖНО! Полностью удаляет всю информацию выбранного отеля!</h1>"
)
def delete_hotel(hotel_id: int = Path(description="Уникальный идентификатор")):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
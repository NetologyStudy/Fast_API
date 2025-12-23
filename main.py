import uvicorn
from fastapi import FastAPI, Query


app = FastAPI()


hotels = [
    {"id": 1, "title": "Sochi"},
    {"id": 2, "title": "Дубай"}
]


@app.get("/hotels")
def get_hotels(
        id: int | None= Query(None, description= "Идентификатор отеля"),
        title: str | None = Query(None, description= "Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.get("/")
def func():
    return "Hello, World!"



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
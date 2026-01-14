from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str
    location: str
    stars: int


class Hotel(HotelAdd):
    id: int


class HotelPatch(BaseModel):
    title: str | None = None
    location: str | None = None
    stars: int | None = None
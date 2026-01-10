from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str
    location: str
    stars: int


class Hotel(HotelAdd):
    id: int


class HotelPATCH(BaseModel):
    title: str | None = Field(None)
    location: str | None = Field(None)
    stars: int | None = Field(None)
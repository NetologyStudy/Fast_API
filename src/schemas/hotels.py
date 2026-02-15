from pydantic import BaseModel, Field


class HotelAdd(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    location: str = Field(min_length=1, max_length=100)
    stars: int = Field(gt=0, le=5)


class Hotel(HotelAdd):
    id: int


class HotelPatch(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=100)
    location: str | None = Field(None, min_length=1, max_length=100)
    stars: int | None = Field(None, min_length=1, max_length=100)
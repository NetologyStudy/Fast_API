from datetime import date

from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel


    async def get_all(
            self,
            location,
            title,
            stars,
            limit,
            offset
    ):
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.icontains(location.strip()))
        if title:
            query = query.filter(HotelsOrm.title.icontains(title.strip()))
        if stars:
            query = query.filter(HotelsOrm.stars.contains(stars.strip()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [Hotel.model_validate(model, from_attributes=True) for model in result.scalars().all()]


    async def get_filtered_by_time(
            self,
            date_from: date,
            date_to: date,
    ):

        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to)
        hotels_ids_to_get = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .filter(RoomsOrm.id.in_(rooms_ids_to_get))
        )

        return await self.get_filtered(HotelsOrm.id.in_(hotels_ids_to_get))
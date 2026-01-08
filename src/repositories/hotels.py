from sqlalchemy import select

from src.models.hotels import HotelsOrm
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = Hotel


    async def get_all(
            self,
            location,
            title,
            limit,
            offset
    ):
        query = select(HotelsOrm)
        if location:
            query = query.filter(HotelsOrm.location.icontains(location.strip()))
        if title:
            query = query.filter(HotelsOrm.title.icontains(title.strip()))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(query)
        return [Hotel.model_validate(model, from_attributes=True) for model in result.scalars().all()]
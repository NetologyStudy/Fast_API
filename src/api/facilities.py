from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

router = APIRouter(prefix="/facilities", tags=["Удобства"])

@router.get(
    "",
    summary="Получение всех данных",
    description="<h1>Позволяет получить полную информацию о всех удобствах</h1>"
)
async def get(db: DBDep):
    return await db.facilities.get_all()


@router.post(
    "",
    summary="Добавлениие новых данных",
    description="<h1>Позволяет добавиить новые удобства</h1>"
)
async def create_facility(db: DBDep, facilities_data: FacilityAdd = Body(openapi_examples={
    "1": {"summary": "test_1", "value":{
        "title": "Массаж"
    }},
    "2": {"summary": "test_2", "value":{
        "title": "WI-FI"
    }},
})
):
    facility = await db.facilities.add(facilities_data)
    await db.commit()

    return {"status": "OK", "data": facility}
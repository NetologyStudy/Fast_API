from fastapi import APIRouter, Body

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post(
    "/register",
    summary="Регистрация",
    description="Регистрация нового клиента"
)
async def register_user(data: UserRequestAdd):
    hashed_password = "1243sdf342gdsd"
    new_user_data = UserAdd(first_name=data.first_name,
                            last_name=data.last_name,
                            nickname=data.nickname,
                            email=data.email,
                            hashed_password=hashed_password,
                            )
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()
    return {"status": "OK"}

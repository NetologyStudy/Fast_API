import sqlalchemy
from fastapi import APIRouter, Body

from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__type="id",
    argon2__time_cost=3,
    argon2__memory_cost=65536,
    argon2__parallelism=4
)


@router.post(
    "/register",
    summary="Регистрация",
    description="Регистрация нового клиента"
)
async def register_user(data: UserRequestAdd):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(first_name=data.first_name,
                            last_name=data.last_name,
                            nickname=data.nickname,
                            email=data.email,
                            hashed_password=hashed_password,
                            )
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
        except sqlalchemy.exc.IntegrityError:
            return {"message": "Пользователь с таким email или nickname уже существует"}
        await session.commit()
    return {"status": "OK"}

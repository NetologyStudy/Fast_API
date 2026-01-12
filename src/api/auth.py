import sqlalchemy
from fastapi import APIRouter, Body, HTTPException, Response

from src.api.dependencies import UserIdDep
from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post(
    "/register",
    summary="Регистрация",
    description="<h1>Регистрация нового клиента</h1>"
)
async def register_user(data: UserRequestAdd = Body(openapi_examples={
    "1": {"summary": "test_1", "value": {
        "first_name": "Иван",
        "last_name": "Иванов",
        "nickname": "vano",
        "email": "ivanov@examle.ru",
        "password": "qwerty12345",
    }},
    "2": {"summary": "test_2", "value": {
        "first_name": "Петр",
        "last_name": "Петров",
        "nickname": "petro",
        "email": "petrov@examle.ru",
        "password": "12345qwerty",
    }},
})
):
    hashed_password = AuthService().get_hashed_password(data.password)
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


@router.post(
    "/login",
    summary="Аутентификация пользователя",
    description="<h1>Проверяем есть ли пользователь с таким email в базе</h1>"
)
async def login_user(
        data: UserRequestAdd,
        response: Response
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Полтзователь с таким email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")
    return {"status": "OK"}



@router.get(
    "/me",
    summary="Текущий пользователь",
    description="<h1>Получении информации о текущем пользователе</h1>"
)
async def get_me(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
        return user

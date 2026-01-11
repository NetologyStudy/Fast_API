from datetime import datetime, timedelta, timezone
import sqlalchemy
from fastapi import APIRouter, Body, HTTPException, Response

from pwdlib import PasswordHash
import jwt

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


password_hash = PasswordHash.recommended()
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode |= ({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_hashed_password(password: str) -> str:
    return password_hash.hash(password)


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
    hashed_password = get_hashed_password(data.password)
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
        if not verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}
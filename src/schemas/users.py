from pydantic import BaseModel, Field, EmailStr


class UserRequestAdd(BaseModel):
    first_name: str
    last_name: str
    nickname: str
    email: EmailStr
    password: str


class UserAdd(BaseModel):
    first_name: str
    last_name: str
    nickname: str
    email: EmailStr
    hashed_password: str

class User(BaseModel):
    id: int
    first_name: str
    last_name: str
    nickname: str
    email: EmailStr

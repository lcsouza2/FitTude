from pydantic import BaseModel, EmailStr


class User(BaseModel):
    login_key: str | EmailStr
    password: str

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(User):
    keep_login: bool


class Equipment(BaseModel):
    group_name: str
    equipment_name: str

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserBase):
    name: str


class UserPwdChange(UserBase):
    name: str
    new_password: str


class UserLogin(UserBase):
    keep_login: bool
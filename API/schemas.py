from typing import Optional

from pydantic import BaseModel, EmailStr


class TokenRenew(BaseModel):
    refresh_token: str


class User(BaseModel):
    login_key: str | EmailStr
    password: str


class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(User):
    keep_login: bool


class Aparelho(BaseModel):
    nome_grupamento: str
    nome_aparelho: str

class Musculo(BaseModel):
    nome_grupamento: str
    nome_musculo: str

class Exercicio(BaseModel):
    nome_exercicio: str
    id_aparelho: Optional[int]
    descricao: Optional[str]

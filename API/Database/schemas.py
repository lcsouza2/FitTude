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
    id_musculo: int
    id_aparelho: Optional[int]
    descricao: Optional[str]


class FichaTreino(BaseModel):
    nome_ficha_treino: str
    objetivo_ficha_treino: str


class DivisaoTreino(BaseModel):
    divisao: str
    id_ficha_treino: int


class DivisaoExercicio(BaseModel):
    divisao: str
    id_ficha_treino: int
    id_exercicio: int
    ordem_execucao: int
    series: int
    repeticoes: str | int
    tecnica_avancada: Optional[str]
    descanso: int


class RelatorioTreino(BaseModel):
    divisao: str
    id_ficha_treino: int


class SerieRelatorio(BaseModel):
    divisao: str
    id_ficha_treino: int
    id_exercicio: int
    numero_serie: int
    id_relatorio_treino: int
    repeticoes: str
    carga: int
    observacao: str

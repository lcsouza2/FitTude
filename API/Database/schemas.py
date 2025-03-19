from typing import Optional

from pydantic import BaseModel, EmailStr


class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"


class User(BaseSchema):
    login_key: str | EmailStr
    password: str


class UserRegistro(BaseSchema):
    username: str
    email: EmailStr
    password: str


class UserLogin(User):
    keep_login: bool


class Aparelho(BaseSchema):
    nome_grupamento: str
    nome_aparelho: str


class Musculo(BaseSchema):
    nome_grupamento: str
    nome_musculo: str


class Exercicio(BaseSchema):
    nome_exercicio: str
    id_musculo: int
    id_aparelho: Optional[int]
    descricao: Optional[str]


class FichaTreino(BaseSchema):
    nome_ficha_treino: str
    objetivo_ficha_treino: str


class DivisaoTreino(BaseSchema):
    divisao: str
    id_ficha_treino: int


class DivisaoExercicio(BaseSchema):
    divisao: str
    id_ficha_treino: int
    id_exercicio: int
    ordem_execucao: int
    series: int
    repeticoes: str | int
    tecnica_avancada: Optional[str]
    descanso: int


class RelatorioTreino(BaseSchema):
    divisao: str
    id_ficha_treino: int


class SerieRelatorio(BaseSchema):
    divisao: str
    id_ficha_treino: int
    id_exercicio: int
    numero_serie: int
    id_relatorio_treino: int
    repeticoes: str
    carga: int
    observacao: str


class MusculoAlterar(BaseSchema):
    nome_grupamento: Optional[str] = None
    nome_musculo: Optional[str] = None


class AparelhoAlterar(BaseSchema):
    nome_grupamento: Optional[str]
    nome_aparelho: Optional[str]


class ExercicioAlterar(BaseSchema):
    nome_exercicio: Optional[str]
    id_musculo: Optional[int]
    id_aparelho: Optional[int]
    descricao: Optional[str]


class FichaTreinoAlterar(BaseSchema):
    nome_ficha_treino: Optional[str]
    objetivo_ficha_treino: Optional[str]

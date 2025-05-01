from datetime import date, datetime, timezone
from typing import Optional, Type, TypedDict

from pydantic import BaseModel, EmailStr


class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"


class UserBase(BaseSchema):
    email: EmailStr
    password: str


class UserRegistro(UserBase):
    username: str
    nome: str

class UserPwdChange(BaseSchema):
    new_password: str

class UserLogin(UserBase):
    keep_login: bool


class Grupamento(BaseSchema):
    nome_grupamento: str
    id_usuario: Optional[int]


class GrupamentoAlterar(BaseSchema):
    nome_grupamento: str


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
    data_relatorio: date = datetime.now(timezone.utc).date()
    divisao: str
    id_ficha_treino: int


class SerieRelatorio(BaseSchema):
    divisao: str
    id_ficha_treino: int
    id_exercicio: int
    ordem_execucao: int
    numero_serie: int
    id_relatorio_treino: int
    repeticoes: str
    carga: int
    observacao: str


class MusculoAlterar(BaseSchema):
    nome_grupamento: Optional[str] = None
    nome_musculo: Optional[str] = None


class AparelhoAlterar(BaseSchema):
    nome_grupamento: Optional[str] = None
    nome_aparelho: Optional[str] = None


class ExercicioAlterar(BaseSchema):
    nome_exercicio: Optional[str] = None
    id_musculo: Optional[int] = None
    id_aparelho: Optional[int] = None
    descricao: Optional[str] = None


class FichaTreinoAlterar(BaseSchema):
    nome_ficha_treino: Optional[str] = None
    objetivo_ficha_treino: Optional[str] = None


class DivisaoExercicioAlterar(BaseSchema):
    divisao: str
    id_ficha_treino: int
    id_exercicio: int
    ordem_execucao_atual: int  # ordem de execução no banco de dados
    ordem_execucao: Optional[int]  # nova ordem de execução do exercício
    series: Optional[int] = None
    repeticoes: Optional[str] = None
    tecnica_avancada: Optional[str] = None
    descanso: Optional[int] = None


class DivisaoExercicioInativar(BaseSchema):
    divisao: str
    id_ficha_treino: int
    id_exercicio: int
    ordem_execucao: int


class ConstraintErrorHandling(TypedDict):
    constraint: str
    error: Type[Exception]
    message: str

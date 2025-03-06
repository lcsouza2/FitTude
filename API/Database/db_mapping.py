from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry

reg = registry()


@reg.mapped_as_dataclass
class Grupamento:
    __tablename__ = "grupamento"

    nome_grupamento: Mapped[str] = mapped_column(primary_key=True)


@reg.mapped_as_dataclass
class Usuario:
    __tablename__ = "usuario"

    id_usuario: Mapped[int] = mapped_column(primary_key=True, init=False)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str]


@reg.mapped_as_dataclass
class Musculo:
    __tablename__ = "musculo"

    id_musculo: Mapped[int] = mapped_column(primary_key=True, init=False)
    nome_grupamento: Mapped[str] = mapped_column(
        ForeignKey("grupamento.nome_grupamento"), unique=True
    )
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuario.id_usuario"), unique=True, nullable=True
    )
    nome_musculo: Mapped[str] = mapped_column(unique=True)


@reg.mapped_as_dataclass
class Aparelho:
    __tablename__ = "aparelho"

    id_aparelho: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuario.id_usuario"), unique=True, nullable=True
    )
    nome_grupamento: Mapped[str] = mapped_column(
        ForeignKey("grupamento.nome_grupamento"), unique=True
    )
    nome_aparelho: Mapped[str] = mapped_column(unique=True)


@reg.mapped_as_dataclass
class Exercicio:
    __tablename__ = "exercicio"

    id_exercicio: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_musculo: Mapped[int] = mapped_column(
        ForeignKey("musculo.id_musculo"), unique=True
    )
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuario.id_usuario"), unique=True, nullable=True
    )
    id_aparelho: Mapped[int] = mapped_column(
        ForeignKey("aparelho.id_aparelho"), unique=True, nullable=True
    )
    nome_exercicio: Mapped[str] = mapped_column(unique=True)

    descricao: Mapped[str]


@reg.mapped_as_dataclass
class FichaTreino:
    __tablename__ = "ficha_treino"

    id_ficha_treino: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_usuario: Mapped[int] = mapped_column(
        ForeignKey("usuario.id_usuario"), unique=True
    )
    nome_ficha_treino: Mapped[str] = mapped_column(unique=True)
    objetivo_ficha_treino: Mapped[str]


@reg.mapped_as_dataclass
class DivisaoTreino:
    __tablename__ = "divisao_treino"

    divisao: Mapped[str] = mapped_column(primary_key=True)
    id_ficha_treino: Mapped[int] = mapped_column(
        ForeignKey("ficha_treino.id_ficha_treino"), primary_key=True
    )


@reg.mapped_as_dataclass
class DivisaoExercicio:
    __tablename__ = "divisao_exercicio"

    id_ficha_treino: Mapped[int] = mapped_column(
        ForeignKey("divisao_treino.id_ficha_treino"), primary_key=True
    )
    divisao: Mapped[str] = mapped_column(
        ForeignKey("divisao_treino.divisao"), primary_key=True
    )
    id_exercicio: Mapped[int] = mapped_column(
        ForeignKey("exercicio.id_exercicio"), primary_key=True
    )
    ordem_execucao: Mapped[int] = mapped_column(primary_key=True)
    series: Mapped[int]
    repeticoes: Mapped[str]
    tecnica_avancada: Mapped[str] = mapped_column(nullable=True)
    descanso: Mapped[int]


@reg.mapped_as_dataclass
class RelatorioTreino:
    __tablename__ = "relatorio_treino"

    data_relatorio: Mapped[date]
    id_relatorio_treino: Mapped[int] = mapped_column(primary_key=True, init=False)
    id_ficha_treino: Mapped[int] = ForeignKey("divisao_treino.id_ficha_treino")
    divisao: Mapped[str] = ForeignKey("divisao_treino.divisao")


@reg.mapped_as_dataclass
class SerieRelatorio:
    __tablename__ = "serie_relatorio"

    id_relatorio_treino: Mapped[int] = mapped_column(
        ForeignKey("relatorio_treino.id_relatorio_treino"), primary_key=True
    )
    id_exercicio: Mapped[int] = mapped_column(
        ForeignKey("divisao_exercicio.id_exercicio"), primary_key=True
    )
    divisao: Mapped[str] = mapped_column(
        ForeignKey("divisao_exercicio.divisao"), primary_key=True
    )
    id_ficha_treino: Mapped[int] = mapped_column(
        ForeignKey("divisao_exercicio.id_ficha_treino"), primary_key=True
    )
    numero_serie: Mapped[int] = mapped_column(primary_key=True)
    reps: Mapped[int]
    carga: Mapped[int]
    observacao: Mapped[str] = mapped_column(nullable=True)

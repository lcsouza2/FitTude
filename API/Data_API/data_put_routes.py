from Data_API.data_post_routes import DATA_API
import Database.db_mapping as tables
from Database import schemas
from Database.utils import AsyncSession, validar_token, excluir_falsy_dict
from sqlalchemy import update, and_
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException, Depends, Query

from http.client import CONFLICT, NOT_FOUND


@DATA_API.put("/muscle/update/{id_musculo}")
async def alterar_musculo(
    id_musculo: int,
    alteracoes: schemas.MusculoAlterar,
    id_usuario: int = Depends(validar_token),
):
    async with AsyncSession() as sessao:
        try:
            await sessao.begin()
            await sessao.execute(
                update(tables.Musculo)
                .where(
                    and_(
                        tables.Musculo.id_musculo == id_musculo,
                        tables.Musculo.id_usuario == id_usuario,
                    )
                )
                .values(excluir_falsy_dict(alteracoes.model_dump(exclude_none=True)))
            )
        except IntegrityError as erro:
            await sessao.rollback()
            if "uq_musculo" in str(erro):
                raise HTTPException(
                    CONFLICT,
                    "Os dados recebidos conflitam com algum registro existente!",
                )
            elif "fk_musculo_grupamento" in str(erro):
                raise HTTPException(
                    NOT_FOUND, "O grupamento referenciado não foi encontrado"
                )
        else:
            await sessao.commit()


@DATA_API.put("/equipment/update/{id_aparelho}")
async def alterar_aparelho(
    id_aparelho: int,
    alteracoes: schemas.AparelhoAlterar,
    id_usuario: int = Depends(validar_token),
):
    async with AsyncSession() as sessao:
        try:
            await sessao.begin()
            await sessao.execute(
                update(tables.Aparelho)
                .where(
                    and_(
                        tables.Aparelho.id_aparelho == id_aparelho,
                        tables.Aparelho.id_usuario == id_usuario,
                    )
                )
                .values(excluir_falsy_dict(alteracoes.model_dump(exclude_none=True)))
            )
        except IntegrityError as erro:
            await sessao.rollback()
            if "uq_aparelho" in str(erro):
                raise HTTPException(
                    CONFLICT,
                    "Os dados recebidos conflitam com algum registro existente!",
                )
            elif "fk_aparelho_grupamento" in str(erro):
                raise HTTPException(
                    NOT_FOUND, "O grupamento referenciado não foi encontrado"
                )
        else:
            await sessao.commit()


@DATA_API.put("/exercise/update/{id_exercicio}")
async def alterar_exercicio(
    id_exercicio: int,
    alteracoes: schemas.ExercicioAlterar,
    id_usuario: int = Depends(validar_token),
):
    async with AsyncSession() as sessao:
        try:
            await sessao.begin()
            await sessao.execute(
                update(tables.Exercicio)
                .where(
                    and_(
                        tables.Exercicio.id_exercicio == id_exercicio,
                        tables.Exercicio.id_usuario == id_usuario,
                    )
                )
                .values(excluir_falsy_dict(alteracoes.model_dump(exclude_none=True)))
            )
        except IntegrityError as erro:
            await sessao.rollback()
            if "uq_exercicio" in str(erro):
                raise HTTPException(
                    CONFLICT,
                    "Os dados recebidos conflitam com algum registro existente!",
                )
            elif "fk_exercicio_aparelho" in str(erro):
                raise HTTPException(
                    NOT_FOUND, "O aparelho referenciado não foi encontrado "
                )
            elif "fk_exercicio_musculo" in str(erro):
                raise HTTPException(
                    NOT_FOUND, "O músculo referenciado não foi encontrado "
                )

        else:
            await sessao.commit()


@DATA_API.put("workout/sheet/update/{id_ficha_treino}")
async def alterar_ficha_treino(
    id_ficha_treino: int,
    alteracoes: schemas.FichaTreinoAlterar,
    id_usuario: int = Depends(validar_token),
):
    async with AsyncSession() as sessao:
        try:
            await sessao.begin()
            await sessao.execute(
                update(tables.FichaTreino)
                .where(
                    and_(
                        tables.FichaTreino.id_ficha_treino == id_ficha_treino,
                        tables.FichaTreino.id_usuario == id_usuario,
                    )
                )
                .values(excluir_falsy_dict(alteracoes.model_dump(exclude_none=True)))
            )
        except IntegrityError as erro:
            await sessao.rollback()
            if "uq_ficha_treino" in str(erro):
                raise HTTPException(
                    CONFLICT,
                    "Os dados recebidos conflitam com algum registro existente!",
                )
        else:
            await sessao.commit()


@DATA_API.put("/workout/division/update/{division}")
async def update_workout_division(
    division: str,
    new_division_name: str = Query(),
    user_id: int = Depends(validar_token),
): ...

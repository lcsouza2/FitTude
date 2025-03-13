from Data_API.data_post_routes import DATA_API
import Database.db_mapping as tables
from Database import schemas
from Database.utils import AsyncSession, validar_token, excluir_falsy_dict
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError

from fastapi import Request, Response, HTTPException

from http.client import CONFLICT, NOT_FOUND


@DATA_API.put("/muscle/update/{id_musculo}")
async def alterar_musculo(
    id_musculo: int,
    alteracoes: schemas.MusculoAlterar,
    request: Request,
    response: Response,
):
    await validar_token(request, response)
    async with AsyncSession() as sessao:
        try:
            await sessao.begin()
            await sessao.execute(
                update(tables.Musculo)
                .where(tables.Musculo.id_musculo == id_musculo)
                .values(excluir_falsy_dict(alteracoes.model_dump(exclude_none=True)))
            )
        except IntegrityError as erro:
            if "uq_musculo" in str(erro):
                await sessao.rollback()
                raise HTTPException(
                    CONFLICT,
                    "Os dados recebidos conflitam com algum registro existente!",
                )
            elif "fk_musculo_grupamento" in str(erro):
                raise HTTPException(
                    NOT_FOUND,
                    "O grupamento referenciado não foi encontrado"
                    )
        else:
            await sessao.commit()


@DATA_API.put("/equipment/update/{id_aparelho}")
async def alterar_aparelho(id_aparelho: int, alteracoes: schemas.AparelhoAlterar):
    async with AsyncSession() as sessao:
        try:
            await sessao.begin()
            await sessao.execute(
                update(tables.Aparelho)
                .where(tables.Aparelho.id_aparelho == id_aparelho)
                .values(excluir_falsy_dict(alteracoes.model_dump(exclude_none=True)))
            )
        except IntegrityError as erro:
            if "uq_aparelho" in str(erro):
                await sessao.rollback()
                raise HTTPException(
                    CONFLICT,
                    "Os dados recebidos conflitam com algum registro existente!",
                )
            elif "fk_aparelho_grupamento" in str(erro):
                raise HTTPException(
                    NOT_FOUND,
                    "O grupamento referenciado não foi encontrado"
                    )
        else:
            await sessao.commit()


@DATA_API.put("/exercise/update/{id_exercicio}")
async def alterar_exercicio(id_exercicio: int, alteracoes: schemas.ExercicioAlterar):
    async with AsyncSession() as sessao:
        try:
            await sessao.begin()
            await sessao.execute(
                update(tables.Exercicio)
                .where(tables.Exercicio.id_exercicio == id_exercicio)
                .values(excluir_falsy_dict(alteracoes.model_dump(exclude_none=True)))
            )
        except IntegrityError as erro:
            if "uq_exercicio" in str(erro):
                await sessao.rollback()
                raise HTTPException(
                    CONFLICT,
                    "Os dados recebidos conflitam com algum registro existente!",
                )
            elif "fk_exercicio_aparelho" in str(erro):
                await sessao.rollback()
                raise HTTPException(
                    NOT_FOUND,
                    "O aparelho referenciado não foi encontrado "
                )
            elif "fk_exercicio_musculo" in str(erro):
                await sessao.rollback()
                raise HTTPException(
                    NOT_FOUND,
                    "O músculo referenciado não foi encontrado "
                )

        else:
            await sessao.commit()

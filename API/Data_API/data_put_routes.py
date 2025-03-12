from Data_API.data_post_routes import DATA_API
import Database.db_mapping as tables
from Database import schemas
from Database.utils import AsyncSession, validar_token
from sqlalchemy import update
from sqlalchemy.exc import NoSuchColumnError, IntegrityError

from fastapi import Request, Response, HTTPException

from http.client import CONFLICT, BAD_REQUEST


@DATA_API.put("/muscle/update/{id_musculo}")
async def alterar_musculo(
    id_musculo: int, alteracoes: schemas.MusculoAlterar, request: Request, response: Response
):
    await validar_token(request, response)
    async with AsyncSession() as sessao:
        try:
            await sessao.begin()
            await sessao.execute(
                update(tables.Musculo)
                .where(tables.Musculo.id_musculo == id_musculo)
                .values(alteracoes.model_dump(exclude_none=True))
            )
        except IntegrityError as erro:
            if "uq_musculo" in str(erro):
                await sessao.rollback()
                raise HTTPException(CONFLICT, "Os dados recebidos conflitam com algum registro existente!")
        except NoSuchColumnError:
            raise HTTPException(BAD_REQUEST,  "Recebido um atributo inexistente")
        else:
            await sessao.commit()

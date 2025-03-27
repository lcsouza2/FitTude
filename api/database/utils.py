from http.client import NOT_FOUND

from database import db_mapping as tables
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from core.connections import AsyncSession

async def get_user_id_by_email(email_usuario: EmailStr):
    async with AsyncSession() as session:
        result = await session.scalars(
            select(tables.Usuario.id_usuario).where(
                tables.Usuario.email == email_usuario
            )
        )
        try:
            return str(result.one())
        except NoResultFound:
            raise HTTPException(NOT_FOUND, "Não existe usuário com esse email")


def exclude_falsy_from_dict(payload: dict):
    return {key: value for key, value in payload.items() if value}

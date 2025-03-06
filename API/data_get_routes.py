from data_post_routes import DATA_API
from Database import db_mapping as tables
from Database.utils import AsyncSession, validate_token
from fastapi import Request, Response
from sqlalchemy import or_, select


@DATA_API.get("/exercise/get")
async def buscar_todos_os_exercicios(request: Request, response: Response):
    """Valida o token e busca os exercicios relativos aquele usuário"""

    id_usuario = validate_token(request, response)

    async with AsyncSession() as session:
        exercicios = await session.scalars(
            select(tables.Exercicio).where(
                or_(
                    tables.Exercicio.id_usuario == id_usuario,
                    tables.Exercicio.id_usuario == None,
                )
            )
        )

    return exercicios.fetchall()


@DATA_API.get("/muscle/get")
async def buscar_todos_os_musculos(request: Request, response: Response):
    """Busca os músuclos referentes a um usuário e retorna eles"""
    # id_usuario = await

    id_usuario = await validate_token(request, response)

    async with AsyncSession() as session:
        musculos = await session.scalars(
            select(tables.Musculo).where(
                or_(
                    tables.Musculo.id_usuario == id_usuario,
                    tables.Musculo.id_usuario == None,
                )
            )
        )

    return musculos.fetchall()


@DATA_API.get("/equipment/get")
async def buscar_todos_os_musculos(request: Request, response: Response):
    """Busca os músuclos referentes a um usuário e retorna eles"""
    # id_usuario = await

    id_usuario = await validate_token(request, response)

    async with AsyncSession() as session:
        aparelhos = await session.scalars(
            select(tables.Aparelho).where(
                or_(
                    tables.Aparelho.id_usuario == id_usuario,
                    tables.Aparelho.id_usuario == None,
                )
            )
        )

    return aparelhos.fetchall()

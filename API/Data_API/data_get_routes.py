from Data_API.data_post_routes import DATA_API
from Database import db_mapping as tables
from Database.utils import AsyncSession, validate_token
from fastapi import Request, Response
from sqlalchemy import or_, select, and_


@DATA_API.get("/groups/get")
async def buscar_todos_os_grupamentos(request: Request, response: Response):
    await validate_token(request, response)

    async with AsyncSession() as session:
        grupamentos = await session.scalars(select(tables.Grupamento))

    return grupamentos.fetchall()


@DATA_API.get("/muscle/get")
async def buscar_todos_os_musculos(request: Request, response: Response):
    """Busca os músuclos referentes a um usuário e retorna eles"""

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


@DATA_API.get("/exercise/get")
async def buscar_todos_os_exercicios(request: Request, response: Response):
    """Valida o token e busca os exercicios relativos aquele usuário"""

    id_usuario = await validate_token(request, response)

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


@DATA_API.get("/workout/sheet/get")
async def buscar_todas_fichas_treino(request: Request, response: Response):
    id_usuario = await validate_token(request, response)

    async with AsyncSession() as session:
        fichas = await session.scalars(
            select(tables.FichaTreino).where(
                tables.FichaTreino.id_usuario == id_usuario,
            )
        )

    return fichas.fetchall()


@DATA_API.get("/workout/sheet/get_divisions")
async def buscar_todas_divisoes_treino(request: Request, response: Response):
    id_usuario = await validate_token(request, response)

    async with AsyncSession() as session:
        fichas = await session.scalars(
            select(tables.DivisaoTreino)
            .join(tables.FichaTreino)
            .where(tables.FichaTreino.id_usuario == id_usuario)
        )
    return fichas.fetchall()


@DATA_API.get("/workout/sheet/get_exercises")
async def buscar_todos_exercicios_divisao(request: Request, response: Response):
    id_usuario = await validate_token(request, response)

    async with AsyncSession() as session:
        fichas = await session.scalars(
            select(tables.DivisaoExercicio)
            .join(
                tables.DivisaoTreino,
                tables.DivisaoTreino.divisao
                == tables.DivisaoExercicio.divisao,
            )
            .join(tables.FichaTreino)
            .where(tables.FichaTreino.id_usuario == id_usuario)
        )

    return fichas.fetchall()

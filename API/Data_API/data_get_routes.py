from Database import db_mapping as tables
from Database.utils import AsyncSession, validate_token
from fastapi import Depends, FastAPI
from sqlalchemy import or_, select

DATA_API = FastAPI(title="Rotas POST para serviços de treinos")


@DATA_API.get("/groups/get")
async def get_all_muscular_groups(user_id: int = Depends(validate_token)):
    async with AsyncSession() as session:
        groups = await session.scalars(select(tables.Grupamento))

    return groups.fetchall()


@DATA_API.get("/muscle/get")
async def get_all_muscles(user_id: int = Depends(validate_token)):
    """Busca os músuclos referentes a um usuário e retorna eles"""

    async with AsyncSession() as session:
        muscles = await session.scalars(
            select(tables.Musculo).where(
                or_(
                    tables.Musculo.id_usuario == user_id,
                    tables.Musculo.id_usuario == None,
                )
            )
        )

    return muscles.fetchall()


@DATA_API.get("/equipment/get")
async def get_all_equipments(user_id: int = Depends(validate_token)):
    """Busca os músuclos referentes a um usuário e retorna eles"""

    async with AsyncSession() as session:
        equipments = await session.scalars(
            select(tables.Aparelho).where(
                or_(
                    tables.Aparelho.id_usuario == user_id,
                    tables.Aparelho.id_usuario == None,
                )
            )
        )

    return equipments.fetchall()


@DATA_API.get("/exercise/get")
async def get_all_exercises(user_id: int = Depends(validate_token)):
    """Valida o token e busca os exercicios relativos aquele usuário"""

    async with AsyncSession() as session:
        exercises = await session.scalars(
            select(tables.Exercicio).where(
                or_(
                    tables.Exercicio.id_usuario == user_id,
                    tables.Exercicio.id_usuario == None,
                )
            )
        )

    return exercises.fetchall()


@DATA_API.get("/workout/sheet/get")
async def get_all_workout_sheets(user_id: int = Depends(validate_token)):
    async with AsyncSession() as session:
        sheets = await session.scalars(
            select(tables.FichaTreino).where(
                tables.FichaTreino.id_usuario == user_id,
            )
        )

    return sheets.fetchall()


@DATA_API.get("/workout/sheet/get_divisions")
async def get_all_workout_divisions(user_id: int = Depends(validate_token)):
    async with AsyncSession() as session:
        sheets = await session.scalars(
            select(tables.DivisaoTreino)
            .join(tables.FichaTreino)
            .where(tables.FichaTreino.id_usuario == user_id)
        )
    return sheets.fetchall()


@DATA_API.get("/workout/sheet/get_exercises")
async def get_all_division_exercises(user_id: int = Depends(validate_token)):
    async with AsyncSession() as session:
        sheets = await session.scalars(
            select(tables.DivisaoExercicio)
            .join(
                tables.DivisaoTreino,
                tables.DivisaoTreino.divisao == tables.DivisaoExercicio.divisao,
            )
            .join(tables.FichaTreino)
            .where(tables.FichaTreino.id_usuario == user_id)
        )

    return sheets.fetchall()

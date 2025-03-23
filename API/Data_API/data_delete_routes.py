from http.client import NOT_FOUND

import Database.db_mapping as tables
from Data_API.data_put_routes import DATA_API
from Database import schemas
from Database.utils import AsyncSession, validate_token
from fastapi import Depends, HTTPException
from sqlalchemy import and_, delete, update


@DATA_API.delete("/muscle/inactivate/{muscle_id}")
async def inactivate_muscle(muscle_id: int, user_id: int = Depends(validate_token)):
    async with AsyncSession() as session:
        result = await session.execute(
            update(tables.Musculo)
            .where(
                and_(
                    tables.Musculo.id_musculo == muscle_id,
                    tables.Musculo.id_usuario == user_id,
                )
            )
            .values(ativo=False)
            .returning(tables.Musculo.id_musculo)
        )

        if result.scalar_one_or_none() is None:
            raise HTTPException(NOT_FOUND, "Músculo não encontrado")
        await session.commit()


@DATA_API.delete("/equipment/inactivate/{equipment_id}")
async def inactivate_equipment(
    equipment_id: int, user_id: int = Depends(validate_token)
):
    async with AsyncSession() as session:
        result = await session.execute(
            update(tables.Aparelho)
            .where(
                and_(
                    tables.Aparelho.id_aparelho == equipment_id,
                    tables.Aparelho.id_usuario == user_id,
                )
            )
            .values(ativo=False)
            .returning(tables.Aparelho.id_aparelho)
        )

        if result.scalar_one_or_none() is None:
            raise HTTPException(NOT_FOUND, "Aparelho não encontrado")
        await session.commit()


@DATA_API.delete("/exericse/inactivate/{exercise_id}")
async def inactivate_exercise(exercise_id: int, user_id: int = Depends(validate_token)):
    async with AsyncSession() as session:
        result = await session.execute(
            update(tables.Exercicio)
            .where(
                and_(
                    tables.Exercicio.id_exercicio == exercise_id,
                    tables.Exercicio.id_usuario == user_id,
                )
            )
            .values(ativo=False)
            .returning(tables.Exercicio.id_exercicio)
        )

        if result.scalar_one_or_none() is None:
            raise HTTPException(NOT_FOUND, "Exercício não encontrado")
        await session.commit()


@DATA_API.delete("/workout/sheet/inactivate/{sheet_id}")
async def inactivate_workout_sheet(
    sheet_id: int, user_id: int = Depends(validate_token)
):
    async with AsyncSession() as session:
        result = await session.execute(
            update(tables.FichaTreino)
            .where(
                and_(
                    tables.FichaTreino.id_ficha_treino == sheet_id,
                    tables.FichaTreino.id_usuario == user_id,
                )
            )
            .values(ativo=False)
            .returning(tables.FichaTreino.id_ficha_treino)
        )

        if result.scalar_one_or_none() is None:
            raise HTTPException(NOT_FOUND, "Ficha de treino não encontrada")
        await session.commit()


@DATA_API.delete("/workout/division/inactivate/{division}")
async def inactivate_workout_division(
    division: str, user_id: int = Depends(validate_token)
):
    async with AsyncSession() as session:
        result = await session.execute(
            update(tables.DivisaoTreino)
            .where(
                and_(
                    tables.DivisaoTreino.divisao == division,
                    tables.DivisaoTreino.id_ficha_treino
                    == tables.FichaTreino.id_ficha_treino,
                    tables.FichaTreino.id_usuario == user_id,
                )
            )
            .values(ativo=False)
            .returning(tables.FichaTreino.id_ficha_treino)
        )

        if result.scalar_one_or_none() is None:
            raise HTTPException(NOT_FOUND, "Divisão de treino não encontrada")
        await session.commit()


@DATA_API.delete("/workout/division/exercise/inactivate")
async def inactivate_division_exercise(
    exercise: schemas.DivisaoExercicioInativar, user_id: int = Depends(validate_token)
):
    async with AsyncSession() as session:
        result = await session.execute(
            update(tables.DivisaoExercicio)
            .where(
                and_(
                    tables.DivisaoExercicio.divisao == exercise.divisao,
                    tables.DivisaoExercicio.id_exercicio == exercise.id_exercicio,
                    tables.DivisaoExercicio.ordem_execucao == exercise.ordem_execucao,
                    tables.FichaTreino.id_usuario == user_id,
                    tables.FichaTreino.id_ficha_treino == exercise.id_ficha_treino,
                    # Joins
                    tables.DivisaoExercicio.id_ficha_treino
                    == tables.DivisaoTreino.id_ficha_treino,
                    tables.DivisaoTreino.id_ficha_treino
                    == tables.FichaTreino.id_ficha_treino,
                )
            )
            .values(ativo=False)
            .returning(tables.FichaTreino.id_ficha_treino)
        )

        if result.scalar_one_or_none() is None:
            raise HTTPException(
                NOT_FOUND, "Exercício não encontrado na divisao de treino"
            )
        await session.commit()


@DATA_API.delete("/workout/report/delete/{report_id}")
async def inactivate_division_exercise(
    report_id: int, user_id: int = Depends(validate_token)
):
    async with AsyncSession() as session:
        await session.execute(
            delete(tables.SerieRelatorio).where(
                and_(
                    tables.SerieRelatorio.id_relatorio_treino == report_id,
                    tables.FichaTreino.id_usuario == user_id,
                    # Joins
                    tables.SerieRelatorio.id_relatorio_treino
                    == tables.RelatorioTreino.id_relatorio_treino,
                    tables.RelatorioTreino.id_ficha_treino
                    == tables.FichaTreino.id_ficha_treino,
                )
            )
        )

        result = await session.execute(
            delete(tables.RelatorioTreino)
            .where(
                and_(
                    tables.RelatorioTreino.id_relatorio_treino == report_id,
                    tables.FichaTreino.id_ficha_treino == user_id,
                    # Join
                    tables.RelatorioTreino.id_ficha_treino
                    == tables.FichaTreino.id_ficha_treino,
                )
            )
            .returning(tables.FichaTreino.id_ficha_treino)
        )

        if result.scalar_one_or_none() is None:
            raise HTTPException(NOT_FOUND, "Relatório não encontrado")
        await session.commit()

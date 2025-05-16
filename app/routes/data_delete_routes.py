from fastapi import APIRouter, Depends
from sqlalchemy import BinaryExpression, and_, delete, update
from sqlalchemy.orm import InstrumentedAttribute, MappedAsDataclass

from ..core import schemas
from ..core.authetication import TokenService
from ..core.connections import db_connection
from ..core.exceptions import EntityNotFound

from database import db_mapping

DATA_DELETE_API = APIRouter(prefix="/api/data")


async def _execute_inactivate_entity(
    *,
    table: MappedAsDataclass,
    where_clause: BinaryExpression,
    returning_column: InstrumentedAttribute,
    entity_name: str,
):
    async with db_connection() as session:
        result = await session.execute(
            update(table)
            .values(ativo=False)
            .where(where_clause)
            .returning(returning_column)
        )

        if result.scalar_one_or_none() is None:
            await session.rollback()
            raise EntityNotFound(f"{entity_name} não encontrado(a)")

        await session.commit()

        return f"{entity_name} excluido"


async def _execute_delete(
    *,
    table: MappedAsDataclass,
    where_clause: BinaryExpression,
    returning_column: InstrumentedAttribute,
    entity_name: str,
):
    async with db_connection() as session:
        result = await session.execute(
            delete(table).where(where_clause).returning(returning_column)
        )

        if result.scalar_one_or_none() is None:
            await session.rollback()
            raise EntityNotFound(f"{entity_name} não encontrado(a)")

        await session.commit()

        return f"{entity_name} excluido"


@DATA_DELETE_API.delete("/groups/inactivate/{group_name}")
async def inactivate_group(
    group_name: str, user_id: int = Depends(TokenService.validate_token)
):
    """Inativa um grupamento muscular"""
    where = and_(
        db_mapping.Grupamento.nome_grupamento == group_name,
        db_mapping.Grupamento.id_usuario == user_id,
    )

    returning = db_mapping.Grupamento.nome_grupamento

    await _execute_inactivate_entity(
        table=db_mapping.Grupamento,
        where_clause=where,
        returning_column=returning,
        entity_name="Grupamento",
    )


@DATA_DELETE_API.delete("/muscle/inactivate/{muscle_id}")
async def inactivate_muscle(
    muscle_id: int, user_id: int = Depends(TokenService.validate_token)
):
    where = and_(
        db_mapping.Musculo.id_musculo == muscle_id,
        db_mapping.Musculo.id_usuario == user_id,
    )

    returning = db_mapping.Musculo.id_musculo

    await _execute_inactivate_entity(
        table=db_mapping.Musculo,
        where_clause=where,
        returning_column=returning,
        entity_name="Musculo",
    )


@DATA_DELETE_API.delete("/equipment/inactivate/{equipment_id}")
async def inactivate_equipment(
    equipment_id: int, user_id: int = Depends(TokenService.validate_token)
):
    where = and_(
        db_mapping.Aparelho.id_aparelho == equipment_id,
        db_mapping.Aparelho.id_usuario == user_id,
    )

    returning = db_mapping.Aparelho.id_aparelho

    await _execute_inactivate_entity(
        table=db_mapping.Aparelho,
        where_clause=where,
        returning_column=returning,
        entity_name="Aparelho",
    )


@DATA_DELETE_API.delete("/exericse/inactivate/{exercise_id}")
async def inactivate_exercise(
    exercise_id: int, user_id: int = Depends(TokenService.validate_token)
):
    where = and_(
        db_mapping.Exercicio.id_exercicio == exercise_id,
        db_mapping.Exercicio.id_usuario == user_id,
    )

    returning = db_mapping.Exercicio.id_exercicio

    await _execute_inactivate_entity(
        table=db_mapping.Exercicio,
        where_clause=where,
        returning_column=returning,
        entity_name="Exercício",
    )


@DATA_DELETE_API.delete("/workout/sheet/inactivate/{sheet_id}")
async def inactivate_workout_sheet(
    sheet_id: int, user_id: int = Depends(TokenService.validate_token)
):
    where = and_(
        db_mapping.FichaTreino.id_ficha_treino == sheet_id,
        db_mapping.FichaTreino.id_usuario == user_id,
    )

    returning = db_mapping.FichaTreino.id_ficha_treino

    await _execute_inactivate_entity(
        table=db_mapping.FichaTreino,
        where_clause=where,
        returning_column=returning,
        entity_name="Ficha de treino",
    )


@DATA_DELETE_API.delete("/workout/division/inactivate/{division}")
async def inactivate_workout_division(
    division: str, user_id: int = Depends(TokenService.validate_token)
):
    where = and_(
        db_mapping.DivisaoTreino.divisao == division,
        db_mapping.DivisaoTreino.id_ficha_treino
        == db_mapping.FichaTreino.id_ficha_treino,
        db_mapping.FichaTreino.id_usuario == user_id,
    )

    returning = db_mapping.FichaTreino.id_ficha_treino

    await _execute_inactivate_entity(
        table=db_mapping.DivisaoTreino,
        where_clause=where,
        returning_column=returning,
        entity_name="Divisão de treino",
    )


@DATA_DELETE_API.delete("/workout/division/exercise/inactivate")
async def inactivate_division_exercise(
    exercise: schemas.DivisaoExercicioInativar,
    user_id: int = Depends(TokenService.validate_token),
):
    where = and_(
        db_mapping.DivisaoExercicio.divisao == exercise.divisao,
        db_mapping.DivisaoExercicio.id_exercicio == exercise.id_exercicio,
        db_mapping.DivisaoExercicio.ordem_execucao == exercise.ordem_execucao,
        db_mapping.FichaTreino.id_usuario == user_id,
        db_mapping.FichaTreino.id_ficha_treino == exercise.id_ficha_treino,
        # Joins
        db_mapping.DivisaoExercicio.id_ficha_treino
        == db_mapping.DivisaoTreino.id_ficha_treino,
        db_mapping.DivisaoTreino.id_ficha_treino
        == db_mapping.FichaTreino.id_ficha_treino,
    )

    returning = db_mapping.FichaTreino.id_ficha_treino

    await _execute_inactivate_entity(
        table=db_mapping.DivisaoExercicio,
        where_clause=where,
        returning_column=returning,
        entity_name="Exercício na divisao de treino",
    )


@DATA_DELETE_API.delete("/workout/report/delete/{report_id}")
async def delete_workout_report(
    report_id: int, user_id: int = Depends(TokenService.validate_token)
):
    # First delete the series reports
    where_series = and_(
        db_mapping.SerieRelatorio.id_relatorio_treino == report_id,
        db_mapping.FichaTreino.id_usuario == user_id,
        # Joins
        db_mapping.SerieRelatorio.id_relatorio_treino
        == db_mapping.RelatorioTreino.id_relatorio_treino,
        db_mapping.RelatorioTreino.id_ficha_treino
        == db_mapping.FichaTreino.id_ficha_treino,
    )

    await _execute_delete(
        table=db_mapping.SerieRelatorio,
        where_clause=where_series,
        returning_column=db_mapping.SerieRelatorio.id_relatorio_treino,
        entity_name="Séries do relatório",
    )

    # Then delete the workout report
    where_report = and_(
        db_mapping.RelatorioTreino.id_relatorio_treino == report_id,
        db_mapping.FichaTreino.id_usuario == user_id,
        # Join
        db_mapping.RelatorioTreino.id_ficha_treino
        == db_mapping.FichaTreino.id_ficha_treino,
    )

    await _execute_delete(
        table=db_mapping.RelatorioTreino,
        where_clause=where_report,
        returning_column=db_mapping.RelatorioTreino.id_relatorio_treino,
        entity_name="Relatório",
    )

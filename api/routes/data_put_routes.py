from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Path
from sqlalchemy import and_, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import InstrumentedAttribute, MappedAsDataclass
from sqlalchemy.sql.expression import BinaryExpression

from core import schemas
from core.authetication import TokenService
from core.connections import db_connection
from core.exceptions import (
    EntityNotFound,
    ForeignKeyViolation,
    PrimaryKeyViolation,
    UniqueConstraintViolation,
)
from core.utils import exclude_falsy_from_dict

from ..database import db_mapping

DATA_PUT_API = APIRouter(prefix="/api/data")


async def _execute_update(
    *,
    table: MappedAsDataclass,
    entity_name: str,
    where_clause: BinaryExpression,
    values_mapping: Dict[InstrumentedAttribute, Any],
    error_mapping: List[schemas.ConstraintErrorHandling],
    returning_column: Optional[InstrumentedAttribute] = None,
):
    """
    Executa uma operação de atualização genérica no banco de dados.

    Args:
        table: Classe do modelo SQLAlchemy a ser atualizado
        entity_name: Nome da entidade para mensagens de erro
        where_clause: Condição WHERE da query
        values_mapping: Dicionário com os valores a serem atualizados
        error_mapping: Lista de mapeamentos de erros de constraint
        returning_column: Coluna a ser retornada após atualização

    Returns:
        str: Mensagem de sucesso "Alterado"

    Raises:
        EntityNotFound: Se o registro não for encontrado
        IntegrityError: Para violações de constraint do banco
    """
    async with db_connection() as session:
        try:
            result = await session.execute(
                update(table)
                .where(where_clause)
                .values(values_mapping)
                .returning(returning_column)
            )
        except IntegrityError as exc:
            await session.rollback()
            for error in error_mapping:
                if error.get("constraint") in str(exc):
                    raise error.get("error")(error.get("message"))
        else:
            if result.scalar_one_or_none() is None:
                await session.rollback()
                raise EntityNotFound(f"{entity_name} não encontrado(a)")

            await session.commit()
            return "Alterado"


@DATA_PUT_API.put("/groups/update/{group_name}")
async def update_group(
    group_name: str,
    updates: schemas.GrupamentoAlterar,
    user_id: int = Depends(TokenService.validate_token),
):
    """Atualiza um grupamento muscular existente"""
    await _execute_update(
        table=db_mapping.Grupamento,
        entity_name="Grupamento",
        where_clause=and_(
            db_mapping.Grupamento.nome_grupamento == group_name,
            db_mapping.Grupamento.id_usuario == user_id,
        ),
        values_mapping=exclude_falsy_from_dict(updates.model_dump(exclude_none=True)),
        error_mapping=[
            {
                "constraint": "uq_grupamento",
                "error": UniqueConstraintViolation,
                "message": "Os dados recebidos conflitam com algum registro existente!",
            },
            {
                "constraint": "fk_grupamento_usuario",
                "error": ForeignKeyViolation,
                "message": "O usuário referenciado não foi encontrado",
            },
        ],
        returning_column=db_mapping.Grupamento.nome_grupamento,
    )


@DATA_PUT_API.put("/muscle/update/{muscle_id}")
async def update_muscle(
    muscle_id: int,
    updates: schemas.MusculoAlterar,
    user_id: int = Depends(TokenService.validate_token),
):
    await _execute_update(
        table=db_mapping.Musculo,
        entity_name="Músculo",
        where_clause=and_(
            db_mapping.Musculo.id_musculo == muscle_id,
            db_mapping.Musculo.id_usuario == user_id,
        ),
        values_mapping=exclude_falsy_from_dict(updates.model_dump(exclude_none=True)),
        error_mapping=[
            {
                "constraint": "uq_musculo",
                "error": UniqueConstraintViolation,
                "message": "Os dados recebidos conflitam com algum registro existente!",
            },
            {
                "constraint": "fk_musculo_grupamento",
                "error": ForeignKeyViolation,
                "message": "O grupamento referenciado não foi encontrado",
            },
            {
                "constraint": "fk_musculo_usuario",
                "error": ForeignKeyViolation,
                "message": "O usuário referenciado não foi encontrado",
            },
        ],
        returning_column=db_mapping.Musculo.id_musculo,
    )


@DATA_PUT_API.put("/equipment/update/{equipment_id}")
async def update_equipment(
    equipment_id: int,
    updates: schemas.AparelhoAlterar,
    user_id: int = Depends(TokenService.validate_token),
):
    await _execute_update(
        table=db_mapping.Aparelho,
        entity_name="Aparelho",
        where_clause=and_(
            db_mapping.Aparelho.id_aparelho == equipment_id,
            db_mapping.Aparelho.id_usuario == user_id,
        ),
        values_mapping=exclude_falsy_from_dict(updates.model_dump(exclude_none=True)),
        error_mapping=[
            {
                "constraint": "uq_aparelho",
                "error": UniqueConstraintViolation,
                "message": "Os dados recebidos conflitam com algum registro existente!",
            },
            {
                "constraint": "fk_aparelho_grupamento",
                "error": ForeignKeyViolation,
                "message": "O grupamento referenciado não foi encontrado",
            },
            {
                "constraint": "fk_musculo_aparelho",
                "error": ForeignKeyViolation,
                "message": "O usuário referenciado não foi encontrado",
            },
            {
                "constraint": "fk_aparelho_usuario",
                "error": ForeignKeyViolation,
                "message": "O usuário referenciado não foi encontrado",
            },
        ],
        returning_column=db_mapping.Aparelho.id_aparelho,
    )


@DATA_PUT_API.put("/exercise/update/{exercise_id}")
async def update_exercise(
    exercise_id: int,
    updates: schemas.ExercicioAlterar,
    user_id: int = Depends(TokenService.validate_token),
):
    await _execute_update(
        table=db_mapping.Exercicio,
        entity_name="Exercício",
        where_clause=and_(
            db_mapping.Exercicio.id_exercicio == exercise_id,
            db_mapping.Exercicio.id_usuario == user_id,
        ),
        values_mapping=exclude_falsy_from_dict(updates.model_dump(exclude_none=True)),
        error_mapping=[
            {
                "constraint": "uq_exercicio",
                "error": UniqueConstraintViolation,
                "message": "Os dados recebidos conflitam com algum registro existente!",
            },
            {
                "constraint": "fk_exercicio_aparelho",
                "error": ForeignKeyViolation,
                "message": "O grupamento referenciado não foi encontrado",
            },
            {
                "constraint": "fk_exercicio_musculo",
                "error": ForeignKeyViolation,
                "message": "O Musculo referenciado não foi encontrado",
            },
            {
                "constraint": "fk_exercicio_usuario",
                "error": ForeignKeyViolation,
                "message": "O usuário referenciado não foi encontrado",
            },
        ],
        returning_column=db_mapping.Exercicio.id_exercicio,
    )


@DATA_PUT_API.put("/workout/sheet/update/{sheet_id}")
async def update_workout_sheet(
    sheet_id: int,
    updates: schemas.FichaTreinoAlterar,
    user_id: int = Depends(TokenService.validate_token),
):
    await _execute_update(
        table=db_mapping.FichaTreino,
        entity_name="Ficha de Treino",
        where_clause=and_(
            db_mapping.FichaTreino.id_ficha_treino == sheet_id,
            db_mapping.FichaTreino.id_usuario == user_id,
        ),
        values_mapping=exclude_falsy_from_dict(updates.model_dump(exclude_none=True)),
        error_mapping=[
            {
                "constraint": "uq_ficha_treino",
                "error": UniqueConstraintViolation,
                "message": "Os dados recebidos conflitam com algum registro existente!",
            },
            {
                "constraint": "fk_ficha_treino_usuario",
                "error": ForeignKeyViolation,
                "message": "O usuário referenciado não foi encontrado",
            },
        ],
        returning_column=db_mapping.FichaTreino.id_ficha_treino,
    )


@DATA_PUT_API.put("/workout/division/update/{division}/{new_division_name}")
async def update_workout_division(
    division: str,
    new_division_name: str = Path(min_length=1, max_length=20),
    user_id: int = Depends(TokenService.validate_token),
):
    await _execute_update(
        table=db_mapping.DivisaoTreino,
        entity_name="Divisão de Treino",
        where_clause=and_(
            db_mapping.DivisaoTreino.divisao == division,
            db_mapping.FichaTreino.id_usuario == user_id,
            # Join
            db_mapping.DivisaoTreino.id_ficha_treino
            == db_mapping.FichaTreino.id_ficha_treino,
        ),
        values_mapping={db_mapping.DivisaoTreino.divisao: new_division_name},
        error_mapping=[
            {
                "constraint": "pk_divisao_treino",
                "error": PrimaryKeyViolation,
                "message": "Já existe essa divisão nessa ficha de treino",
            },
            {
                "constraint": "fk_fivisao_treino_ficha_treino",
                "error": ForeignKeyViolation,
                "message": "O ID da ficha de treino recebido não existe",
            },
        ],
        returning_column=db_mapping.FichaTreino.id_ficha_treino,
    )


@DATA_PUT_API.put("/workout/division/exercise/update/")
async def update_division_exercise(
    updates: schemas.DivisaoExercicioAlterar,
    user_id: int = Depends(TokenService.validate_token),
):
    where_query = and_(
        db_mapping.DivisaoExercicio.divisao == updates.divisao,
        db_mapping.DivisaoExercicio.id_exercicio == updates.id_exercicio,
        db_mapping.DivisaoExercicio.ordem_execucao == updates.ordem_execucao_atual,
        db_mapping.FichaTreino.id_usuario == user_id,
        db_mapping.FichaTreino.id_ficha_treino == updates.id_ficha_treino,
        # Joins
        db_mapping.DivisaoExercicio.id_ficha_treino
        == db_mapping.DivisaoTreino.id_ficha_treino,
        db_mapping.DivisaoTreino.id_ficha_treino
        == db_mapping.FichaTreino.id_ficha_treino,
    )

    update_values = updates.model_dump(
        exclude=(
            "ordem_execucao_atual",
            "id_ficha_treino",
            "id_exercicio",
            "divisao",
        )
    )

    await _execute_update(
        table=db_mapping.DivisaoExercicio,
        entity_name="Exercicio da divisão",
        where_clause=where_query,
        values_mapping=update_values,
        error_mapping=[
            {
                "constraint": "pk_divisao_exercicio",
                "error": PrimaryKeyViolation,
                "message": "Esse exercício já existe nessa divisão",
            },
            {
                "constraint": "fk_divisao_exercicio_divisao_treino",
                "error": ForeignKeyViolation,
                "message": "A divisão de treino referenciada não existe",
            },
        ],
        returning_column=db_mapping.FichaTreino.id_ficha_treino,
    )

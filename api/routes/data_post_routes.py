from typing import List, Any, Dict
from sqlalchemy.orm import MappedAsDataclass
from fastapi import Depends, APIRouter
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

from core.exceptions import PrimaryKeyViolation, ForeignKeyViolation, UniqueConstraintViolation
from core.connections import AsyncSession
from core.authetication import TokenService
from core.utils import exclude_falsy_from_dict

from database import db_mapping
from core import schemas

DATA_POST_API = APIRouter(prefix="/api/data")


async def _execute_insert(
    *,
    table: MappedAsDataclass,
    values: Dict[str, Any],
    error_mapping: List[schemas.ConstraintErrorHandling],
    entity_name: str,
) -> str:
    """
    Executa uma operação de inserção genérica no banco de dados.

    Args:
        table: Classe do modelo SQLAlchemy a ser inserido
        values: Dicionário com os valores a serem inseridos
        error_mapping: Lista de dicionários com mapeamento de erros
        entity_name: Nome da entidade para mensagens de erro

    Returns:
        str: Mensagem de sucesso

    Raises:
        HTTPException: Para violações de constraint do banco
    """
    async with AsyncSession() as session:
        try:
            await session.execute(insert(table).values(values))
            await session.commit()
            return f"{entity_name} criado com sucesso"

        except IntegrityError as exc:
            await session.rollback()
            for error in error_mapping:
                if error.get("constraint") in str(exc):
                    raise error.get("error")(error.get("message"))
            # Se não encontrou erro mapeado, re-raise a exceção original
            raise

@DATA_POST_API.post("/groups/new")
async def create_new_group(
    group: schemas.Grupamento, user_id: int = Depends(TokenService.validate_token)
):
    """Adiciona um novo grupamento muscular personalizado pelo usuário"""
    return await _execute_insert(
        table=db_mapping.Grupamento,
        values={**group.model_dump(), "id_usuario": user_id},
        error_mapping=[
            {
                "constraint": "uq_grupamento",
                "error": UniqueConstraintViolation,
                "message": "Esse grupamento já existe"
            },
            {
                "constraint": "fk_grupamento_usuario",
                "error": ForeignKeyViolation,
                "message": "Usuário referenciado não existe"
            }
        ],
        entity_name="Grupamento",
    )

@DATA_POST_API.post("/equipment/new")
async def create_new_equipment(
    equipment: schemas.Aparelho, user_id: int = Depends(TokenService.validate_token)
):
    """
    Tenta criar o aparelho enviado pelo usuário no banco de dados
    """
    return await _execute_insert(
        table=db_mapping.Aparelho,
        values={**equipment.model_dump(), "id_usuario": user_id},
        error_mapping=[
            {
                "constraint": "uq_aparelho",
                "error": UniqueConstraintViolation,
                "message": "Esse aparelho já existe"
            },
            {
                "constraint": "fk_aparelho_usuario",
                "error": ForeignKeyViolation,
                "message": "Usuário referenciado não existe"
            },
            {
                "constraint": "fk_aparelho_grupamento",
                "error": ForeignKeyViolation,
                "message": "O grupamento referenciado não existe"
            }
        ],
        entity_name="Aparelho",
    )


@DATA_POST_API.post("/muscle/new")
async def create_new_muscle(
    muscle: schemas.Musculo, user_id: int = Depends(TokenService.validate_token)
):
    """Adiciona um novo músculo personalizado pelo usuário ao banco de dados"""
    return await _execute_insert(
        table=db_mapping.Musculo,
        values={**muscle.model_dump(), "id_usuario": user_id},
        error_mapping=[
            {
                "constraint": "uq_musculo",
                "error": UniqueConstraintViolation,
                "message": "Esse músculo já existe"
            },
            {
                "constraint": "fk_musculo_usuario",
                "error": ForeignKeyViolation,
                "message": "Usuário referenciado não existe"
            },
            {
                "constraint": "fk_musculo_grupamento",
                "error": ForeignKeyViolation,
                "message": "O grupamento referenciado não existe"
            }
        ],
        entity_name="Musculo",
    )


@DATA_POST_API.post("/exercise/new")
async def create_new_exercise(
    exercise: schemas.Exercicio, user_id: int = Depends(TokenService.validate_token)
):
    """Adiciona um exercício personalizado pelo usuário ao banco de dados"""
    return await _execute_insert(
        table=db_mapping.Exercicio,
        values={**exercise.model_dump(), "id_usuario": user_id},
        error_mapping=[
            {
                "constraint": "uq_exercicio",
                "error": UniqueConstraintViolation,
                "message": "Esse exercício já existe"
            },
            {
                "constraint": "fk_exercicio_usuario",
                "error": ForeignKeyViolation,
                "message": "Usuário referenciado não existe"
            },
            {
                "constraint": "fk_exercicio_aparelho",
                "error": ForeignKeyViolation,
                "message": "O aparelho referenciado não existe"
            },
            {
                "constraint": "fk_exercicio_musculo",
                "error": ForeignKeyViolation,
                "message": "O musculo referenciado não existe"
            }
        ],
        entity_name="Exercicio",
    )


@DATA_POST_API.post("/workout/sheet/new")
async def create_new_workout_sheet(
    sheet: schemas.FichaTreino, user_id: int = Depends(TokenService.validate_token)
):
    """Cria uma nova ficha de treino"""
    return await _execute_insert(
        table=db_mapping.FichaTreino,
        values={**sheet.model_dump(), "id_usuario": user_id},
        error_mapping=[
            {
                "constraint": "uq_ficha_treino",
                "error": UniqueConstraintViolation,
                "message": "Essa ficha de treino já existe"
            },
            {
                "constraint": "fk_ficha_treino_usuario",
                "error": ForeignKeyViolation,
                "message": "O usuario referenciado não existe"
            }
        ],
        entity_name="FichaTreino",
    )


@DATA_POST_API.post("/workout/division/new")
async def criar_nova_divisao_treino(
    division: schemas.DivisaoTreino, user_id: int = Depends(TokenService.validate_token)
):
    """Adiciona uma nova divisão de treino a uma ficha de treino"""
    return await _execute_insert(
        table=db_mapping.DivisaoTreino,
        values=division.model_dump(),
        error_mapping=[
            {
                "constraint": "pk_divisao_treino",
                "error": PrimaryKeyViolation,
                "message": "Essa divisão de treino já existe nessa ficha"
            },
            {
                "constraint": "fk_divisao_treino_ficha_treino",
                "error": ForeignKeyViolation,
                "message": "A ficha de treino referenciada não existe"
            }
        ],
        entity_name="DivisaoTreino",
    )


@DATA_POST_API.post("/workout/division/add_exercise")
async def add_exercise_to_division(
    exercises: List[schemas.DivisaoExercicio], user_id: int = Depends(TokenService.validate_token)
):
    """Adiciona uma lista de exercícios a uma divisão de treino"""

    await _execute_insert(
        table=db_mapping.DivisaoExercicio,
        values=[i.model_dump() for i in exercises],
        error_mapping=[
            {
                "constraint": "pk_divisao_exercicio",
                "error": PrimaryKeyViolation,
                "message": "Esse exercicio já foi adicionado a essa divisão"
            },
            {
                "constraint": "fk_divisao_exercicio_divisao_treino",
                "error": ForeignKeyViolation,
                "message": "A divisão de treino referenciada não existe"
            },
            {
                "constraint": "fk_divisao_exercicio_exercicio",
                "error": ForeignKeyViolation,
                "message": "O exercício referenciado não existe"
            }
        ],
        entity_name="Exercício na divisão"
    )

@DATA_POST_API.post("/workout/report/new_report")
async def create_new_report(
    report: schemas.RelatorioTreino, user_id: int = Depends(TokenService.validate_token)
):
    """Cria um relatório de treino"""
    return await _execute_insert(
        table=db_mapping.RelatorioTreino,
        values=report.model_dump(),
        error_mapping=[
            {
                "constraint": "fk_relatorio_treino_divisao_treino",
                "error": ForeignKeyViolation,
                "message": "A divisão de treino referenciada não existe"
            },
        ],
        entity_name="Relatorio de treino",
    )


@DATA_POST_API.post("/workout/report/add_exercise")
async def add_exercise_to_report(
    exercises: List[schemas.SerieRelatorio], user_id: int = Depends(TokenService.validate_token)
):
    """Adiciona uma lista de exercícios feitos a um relatório de treino"""

    await _execute_insert(
        table=db_mapping.SerieRelatorio,
        values=[exclude_falsy_from_dict(i.model_dump(exclude_none=True)) for i in exercises],
        error_mapping=[
            {
                "constraint": "pk_serie_relatorio",
                "error": PrimaryKeyViolation,
                "message": "Esse exercício já existe nesse relatório"
            },
            {
                "constraint": "fk_serie_relatorio_divisao_exercicio",
                "error": ForeignKeyViolation,
                "message": "Exercício não encontrado na divisão referenciada"
            },
            {
                "constraint": "fk_serie_relatorio_relatorio_treino",
                "error": ForeignKeyViolation,
                "message": "Relatório referenciado não encontrado"
            },
        ],
        entity_name="Série no relatório"
    )



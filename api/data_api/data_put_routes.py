from http.client import CONFLICT, NOT_FOUND

import database.db_mapping as tables
from data_api.data_post_routes import DATA_API
from database import schemas
from database.utils import AsyncSession, exclude_falsy_from_dict, validate_token
from fastapi import Depends, HTTPException, Query
from sqlalchemy import and_, update
from sqlalchemy.exc import IntegrityError


@DATA_API.put("/muscle/update/{muscle_id}")
async def update_muscle(
    muscle_id: int,
    updates: schemas.MusculoAlterar,
    user_id: int = Depends(validate_token),
):
    async with AsyncSession() as session:
        try:
            result = await session.execute(
                update(tables.Musculo)
                .where(
                    and_(
                        tables.Musculo.id_musculo == muscle_id,
                        tables.Musculo.id_usuario == user_id,
                    )
                )
                .values(exclude_falsy_from_dict(updates.model_dump(exclude_none=True)))
                .returning(tables.Musculo.id_musculo)
            )
        except IntegrityError as exc:
            await session.rollback()
            if "uq_musculo" in str(exc):
                raise HTTPException(
                    CONFLICT,
                    "Os dados recebidos conflitam com algum registro existente!",
                )
            elif "fk_musculo_grupamento" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "O grupamento referenciado não foi encontrado"
                )
        else:
            if result.scalar_one_or_none() is None:
                await session.rollback()
                raise HTTPException(NOT_FOUND, "Músculo não encontrado")

            await session.commit()


@DATA_API.put("/equipment/update/{equipment_id}")
async def update_equipment(
    equipment_id: int,
    updates: schemas.AparelhoAlterar,
    user_id: int = Depends(validate_token),
):
    async with AsyncSession() as session:
        try:
            result = await session.execute(
                update(tables.Aparelho)
                .where(
                    and_(
                        tables.Aparelho.id_aparelho == equipment_id,
                        tables.Aparelho.id_usuario == user_id,
                    )
                )
                .values(exclude_falsy_from_dict(updates.model_dump(exclude_none=True)))
                .returning(tables.Aparelho.id_aparelho)
            )
        except IntegrityError as exc:
            await session.rollback()
            if "uq_aparelho" in str(exc):
                raise HTTPException(
                    CONFLICT,
                    "Os dados recebidos conflitam com algum registro existente!",
                )
            elif "fk_aparelho_grupamento" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "O grupamento referenciado não foi encontrado"
                )
        else:
            if result.scalar_one_or_none() is None:
                await session.rollback()
                raise HTTPException(NOT_FOUND, "Aparelho não encontrado")
            await session.commit()


@DATA_API.put("/exercise/update/{exercise_id}")
async def update_exercise(
    exercise_id: int,
    updates: schemas.ExercicioAlterar,
    user_id: int = Depends(validate_token),
):
    async with AsyncSession() as session:
        try:
            result = await session.execute(
                update(tables.Exercicio)
                .where(
                    and_(
                        tables.Exercicio.id_exercicio == exercise_id,
                        tables.Exercicio.id_usuario == user_id,
                    )
                )
                .values(exclude_falsy_from_dict(updates.model_dump(exclude_none=True)))
                .returning(tables.Exercicio.id_exercicio)
            )
        except IntegrityError as exc:
            await session.rollback()
            if "uq_exercicio" in str(exc):
                raise HTTPException(
                    CONFLICT,
                    "Os dados recebidos conflitam com algum registro existente!",
                )
            elif "fk_exercicio_aparelho" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "O aparelho referenciado não foi encontrado "
                )
            elif "fk_exercicio_musculo" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "O músculo referenciado não foi encontrado "
                )

        else:
            if result.scalar_one_or_none() is None:
                await session.rollback()
                raise HTTPException(NOT_FOUND, "Exercício não econtrado")
            await session.commit()


@DATA_API.put("/workout/sheet/update/{sheet_id}")
async def update_workout_sheet(
    sheet_id: int,
    updates: schemas.FichaTreinoAlterar,
    user_id: int = Depends(validate_token),
):
    async with AsyncSession() as session:
        try:
            result = await session.execute(
                update(tables.FichaTreino)
                .where(
                    and_(
                        tables.FichaTreino.id_ficha_treino == sheet_id,
                        tables.FichaTreino.id_usuario == user_id,
                    )
                )
                .values(exclude_falsy_from_dict(updates.model_dump(exclude_none=True)))
                .returning(tables.FichaTreino.id_ficha_treino)
            )
        except IntegrityError as exc:
            await session.rollback()
            if "uq_ficha_treino" in str(exc):
                raise HTTPException(
                    CONFLICT,
                    "O nome da recebido já é usado por outra ficha de treino",
                )
        else:
            if result.scalar_one_or_none() is None:
                raise HTTPException(NOT_FOUND, "Ficha de treino não encontrada")
            await session.commit()


@DATA_API.put("/workout/division/update/{division}")
async def update_workout_division(
    division: str,
    new_division_name: str = Query(
        max_length=20, description="Novo nome da divisão especificada"
    ),
    user_id: int = Depends(validate_token),
):
    async with AsyncSession() as session:
        try:
            result = await session.execute(
                update(tables.DivisaoTreino)
                .where(
                    and_(
                        tables.DivisaoTreino.divisao == division,
                        tables.FichaTreino.id_usuario == user_id,
                        # Join
                        tables.DivisaoTreino.id_ficha_treino
                        == tables.FichaTreino.id_ficha_treino,
                    )
                )
                .values(divisao=new_division_name)
                .returning(tables.FichaTreino.id_ficha_treino)
            )
        except IntegrityError as exc:
            await session.rollback()

            if "pk_divisao_treino" in str(exc):
                raise HTTPException(
                    CONFLICT, "Já existe essa divisão nessa ficha de treino"
                )

            if "fk_fivisao_treino_ficha_treino" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "O ID da ficha de treino recebido não existe"
                )
        else:
            if result.scalar_one_or_none() is None:
                raise HTTPException(NOT_FOUND, "Divisão de treino não encontrada")
            await session.commit()


@DATA_API.put("/workout/division/exercise/update/")
async def update_division_exercise(
    updates: schemas.DivisaoExercicioAlterar,
    user_id: int = Depends(validate_token),
):
    async with AsyncSession() as session:
        try:
            result = await session.execute(
                update(tables.DivisaoExercicio)
                .where(
                    and_(
                        tables.DivisaoExercicio.divisao == updates.divisao,
                        tables.DivisaoExercicio.id_exercicio == updates.id_exercicio,
                        tables.DivisaoExercicio.ordem_execucao
                        == updates.ordem_execucao_atual,
                        tables.FichaTreino.id_usuario == user_id,
                        tables.FichaTreino.id_ficha_treino == updates.id_ficha_treino,
                        # Joins
                        tables.DivisaoExercicio.id_ficha_treino
                        == tables.DivisaoTreino.id_ficha_treino,
                        tables.DivisaoTreino.id_ficha_treino
                        == tables.FichaTreino.id_ficha_treino,
                    )
                )
                .values(
                    updates.model_dump(
                        exclude=(
                            "ordem_execucao_atual",
                            "id_ficha_treino",
                            "id_exercicio",
                            "divisao",
                        )
                    )
                )
                .returning(tables.FichaTreino.id_ficha_treino)
            )

        except IntegrityError as exc:
            if "pk_divisao_exercicio" in str(exc):
                raise HTTPException(CONFLICT, "Esse exercício já existe nessa divisão")

            if "fk_divisao_exercicio_divisao_treino" in str(exc):
                raise HTTPException(
                    NOT_FOUND, "A divisão de treino referenciada não existe"
                )
        else:
            if result.scalar_one_or_none() is None:
                raise HTTPException(NOT_FOUND, "Exercício não encontrado nessa divisão")
            await session.commit()

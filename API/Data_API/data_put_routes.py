from Data_API.data_post_routes import DATA_API
import Database.db_mapping as tables
from Database import schemas
from Database.utils import AsyncSession, validate_token, exclude_falsy_from_dict
from sqlalchemy import update, and_
from sqlalchemy.exc import IntegrityError

from fastapi import HTTPException, Depends, Query

from http.client import CONFLICT, NOT_FOUND


@DATA_API.put("/muscle/update/{muscle_id}")
async def update_muscle(
    muscle_id: int,
    updates: schemas.MusculoAlterar,
    user_id: int = Depends(validate_token),
):
    async with AsyncSession() as session:
        try:
            await session.begin()
            await session.execute(
                update(tables.Musculo)
                .where(
                    and_(
                        tables.Musculo.id_musculo == muscle_id,
                        tables.Musculo.id_usuario == user_id,
                    )
                )
                .values(exclude_falsy_from_dict(updates.model_dump(exclude_none=True)))
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
            await session.commit()


@DATA_API.put("/equipment/update/{equipment_id}")
async def update_equipment(
    equipment_id: int,
    updates: schemas.AparelhoAlterar,
    user_id: int = Depends(validate_token),
):
    async with AsyncSession() as session:
        try:
            await session.begin()
            await session.execute(
                update(tables.Aparelho)
                .where(
                    and_(
                        tables.Aparelho.id_aparelho == equipment_id,
                        tables.Aparelho.id_usuario == user_id,
                    )
                )
                .values(exclude_falsy_from_dict(updates.model_dump(exclude_none=True)))
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
            await session.commit()


@DATA_API.put("/exercise/update/{exercise_id}")
async def update_exercise(
    exercise_id: int,
    updates: schemas.ExercicioAlterar,
    user_id: int = Depends(validate_token),
):
    async with AsyncSession() as session:
        try:
            await session.begin()
            await session.execute(
                update(tables.Exercicio)
                .where(
                    and_(
                        tables.Exercicio.id_exercicio == exercise_id,
                        tables.Exercicio.id_usuario == user_id,
                    )
                )
                .values(exclude_falsy_from_dict(updates.model_dump(exclude_none=True)))
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
            await session.commit()


@DATA_API.put("/workout/sheet/update/{sheet_id}")
async def alterar_ficha_treino(
    sheet_id: int,
    updates: schemas.FichaTreinoAlterar,
    user_id: int = Depends(validate_token),
):
    async with AsyncSession() as session:
        try:
            await session.begin()
            await session.execute(
                update(tables.FichaTreino)
                .where(
                    and_(
                        tables.FichaTreino.id_ficha_treino == sheet_id,
                        tables.FichaTreino.id_usuario == user_id
                    )
                )
                .values(exclude_falsy_from_dict(updates.model_dump(exclude_none=True)))
            )
        except IntegrityError as exc:
            await session.rollback()
            if "uq_ficha_treino" in str(exc):
                raise HTTPException(
                    CONFLICT,
                    "O nome da recebido já é usado por outra ficha de treino",
                )
        else:
            await session.commit()


@DATA_API.put("/workout/division/update/{division}")
async def update_workout_division(
    division: str,
    new_division_name: str = Query(
        max_length=15, description="Novo nome da divisão especificada"
    ),
    user_id: int = Depends(validate_token),
):
    async with AsyncSession() as session:
        try:
            await session.begin()
            await session.execute(
                update(tables.DivisaoTreino)
                .where(
                    and_(
                        tables.DivisaoTreino.divisao == division,
                        tables.DivisaoTreino.id_ficha_treino
                            == tables.FichaTreino.id_ficha_treino,
                        tables.FichaTreino.id_usuario == user_id,
                    )
                )
                .values(divisao=new_division_name)
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
            await session.commit()

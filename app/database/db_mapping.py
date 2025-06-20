from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry

reg = registry()


@reg.mapped_as_dataclass
class MuscleGroup:
    __tablename__ = "muscle_group"

    user_id: Mapped[int] = mapped_column()
    group_name: Mapped[str] = mapped_column(primary_key=True)


@reg.mapped_as_dataclass
class User:
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str]


@reg.mapped_as_dataclass
class Muscle:
    __tablename__ = "muscle"

    muscle_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    group_name: Mapped[str] = mapped_column(
        ForeignKey("muscle_group.group_name"), unique=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id"), unique=True, nullable=True
    )
    muscle_name: Mapped[str] = mapped_column(unique=True)
    active: Mapped[bool] = mapped_column(default=True)


@reg.mapped_as_dataclass
class Equipment:
    __tablename__ = "equipment"

    equipment_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id"), unique=True, nullable=True
    )
    group_name: Mapped[str] = mapped_column(
        ForeignKey("muscle_group.group_name"), unique=True
    )
    equipment_name: Mapped[str] = mapped_column(unique=True)
    active: Mapped[bool] = mapped_column(default=True)


@reg.mapped_as_dataclass
class Exercise:
    __tablename__ = "exercise"

    exercise_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id"), unique=True, nullable=True
    )
    exercise_name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)


@reg.mapped_as_dataclass
class ExerciseMuscle:
    __tablename__ = "exercise_muscle"

    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercise.exercise_id"), primary_key=True
    )
    muscle_id: Mapped[int] = mapped_column(
        ForeignKey("muscle.muscle_id"), primary_key=True
    )


@reg.mapped_as_dataclass
class ExerciseEquipment:
    __tablename__ = "exercise_equipment"

    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercise.exercise_id"), primary_key=True
    )
    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipment.equipment_id"), primary_key=True
    )


@reg.mapped_as_dataclass
class WorkoutPlan:
    __tablename__ = "workout_plan"

    workout_plan_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), unique=True)
    workout_plan_name: Mapped[str] = mapped_column(unique=True)
    workout_plan_goal: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)


@reg.mapped_as_dataclass
class WorkoutSplit:
    __tablename__ = "workout_split"

    split: Mapped[str] = mapped_column(primary_key=True)
    workout_plan_id: Mapped[int] = mapped_column(
        ForeignKey("workout_plan.workout_plan_id"), primary_key=True
    )
    active: Mapped[bool] = mapped_column(default=True)


@reg.mapped_as_dataclass
class SplitExercise:
    __tablename__ = "split_exercise"

    workout_plan_id: Mapped[int] = mapped_column(
        ForeignKey("workout_split.workout_plan_id"), primary_key=True
    )
    split: Mapped[str] = mapped_column(
        ForeignKey("workout_split.split"), primary_key=True
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercise.exercise_id"), primary_key=True
    )
    execution_order: Mapped[int] = mapped_column(primary_key=True)
    sets: Mapped[int]
    reps: Mapped[str]
    advanced_technique: Mapped[str] = mapped_column(nullable=True)
    rest_time: Mapped[int]
    active: Mapped[bool] = mapped_column(default=True)


@reg.mapped_as_dataclass
class WorkoutReport:
    __tablename__ = "workout_report"

    report_date: Mapped[date]
    workout_report_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    workout_plan_id: Mapped[int] = mapped_column(
        ForeignKey("workout_split.workout_plan_id")
    )
    split: Mapped[str] = mapped_column(ForeignKey("workout_split.split"))


@reg.mapped_as_dataclass
class SetReport:
    __tablename__ = "set_report"

    workout_report_id: Mapped[int] = mapped_column(
        ForeignKey("workout_report.workout_report_id"), primary_key=True
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("split_exercise.exercise_id"), primary_key=True
    )
    split: Mapped[str] = mapped_column(
        ForeignKey("split_exercise.split"), primary_key=True
    )
    workout_plan_id: Mapped[int] = mapped_column(
        ForeignKey("split_exercise.workout_plan_id"), primary_key=True
    )
    execution_order: Mapped[int]
    set_number: Mapped[int] = mapped_column(primary_key=True)
    reps: Mapped[str]
    weight: Mapped[int]
    notes: Mapped[str] = mapped_column(nullable=True)

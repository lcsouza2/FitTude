from api.src.models.base_models import BaseOrmModel
from sqlalchemy.orm import Mapped, mapped_column
from api.src.utils.constraints import DatabaseConstraints
from sqlalchemy import ForeignKey


@BaseOrmModel.registry.mapped_as_dataclass
class WorkoutSetReport:
    __tablename__ = "split_set_report"

    workout_report_id: Mapped[int] = mapped_column(
        ForeignKey("workout_report.workout_report_id", name=DatabaseConstraints.SetReport.FK_WORKOUT_REPORT), primary_key=True
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("split_exercise.exercise_id", name=DatabaseConstraints.SetReport.FK_EXERCISE), primary_key=True
    )
    split: Mapped[str] = mapped_column(
        ForeignKey("split_exercise.split", name=DatabaseConstraints.SetReport.FK_SPLIT), primary_key=True
    )
    execution_order: Mapped[int]
    set_number: Mapped[int] = mapped_column(primary_key=True)
    reps: Mapped[str]
    weight: Mapped[float]
    notes: Mapped[str] = mapped_column(nullable=True)

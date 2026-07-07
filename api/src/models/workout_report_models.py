from api.src.utils.constraints import DatabaseConstraints
from api.src.models.base_models import BaseOrmModel
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from sqlalchemy import ForeignKey

@BaseOrmModel.registry.mapped_as_dataclass
class WorkoutReport:
    __tablename__ = "workout_report"

    report_date: Mapped[date] = mapped_column(primary_key=True)
    workout_report_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    workout_plan_id: Mapped[int] = mapped_column(
        ForeignKey("workout_split.workout_plan_id", name=DatabaseConstraints.WorkoutReport.FK_WORKOUT_PLAN),
        primary_key=True
    )
    split: Mapped[str] = mapped_column(ForeignKey("workout_split.split", name=DatabaseConstraints.WorkoutReport.FK_WORKOUT_SPLIT))

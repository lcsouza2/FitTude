from api.src.utils.constraints import DatabaseConstraints
from api.src.models.base_models import BaseOrmModel
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from sqlalchemy import ForeignKeyConstraint

@BaseOrmModel.registry.mapped_as_dataclass
class WorkoutReport:
    __tablename__ = "workout_report"
    __table_args__ = (
        ForeignKeyConstraint(
            ["split", "workout_plan_id"],
            ["workout_split.split", "workout_split.workout_plan_id"],
            name=DatabaseConstraints.WorkoutReport.FK_WORKOUT_PLAN,
        ),
    )

    report_date: Mapped[date] = mapped_column(primary_key=True)
    id: Mapped[int] = mapped_column(primary_key=True, init=False, unique=True)
    workout_plan_id: Mapped[int] = mapped_column(primary_key=True)
    split: Mapped[str] = mapped_column()

from api.src.models.base_models import BaseOrmModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from api.src.utils.constraints import DatabaseConstraints
from datetime import datetime

@BaseOrmModel.registry.mapped_as_dataclass
class WorkoutSplit:
    __tablename__ = "workout_split"

    split: Mapped[str] = mapped_column(primary_key=True)
    workout_plan_id: Mapped[int] = mapped_column(
        ForeignKey("workout_plan.id", name=DatabaseConstraints.WorkoutSplit.FK_WORKOUT_PLAN), primary_key=True
    )
    deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default_factory=datetime.now, nullable=False, init=False)
    deleted_at: Mapped[datetime] = mapped_column(default=None, nullable=True)

from api.src.models.base_models import BaseOrmModel
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from api.src.utils.constraints import DatabaseConstraints

@BaseOrmModel.registry.mapped_as_dataclass
class WorkoutPlan:
    __tablename__ = "workout_plan"
    __table_args__ = (UniqueConstraint("workout_plan_name", "user_id", name=DatabaseConstraints.WorkoutPlan.UNIQUE),)

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", name=DatabaseConstraints.WorkoutPlan.FK_USER))
    workout_plan_name: Mapped[str] = mapped_column()
    workout_plan_goal: Mapped[str]
    deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False, init=False)
    deleted_at: Mapped[datetime] = mapped_column(default=None, nullable=True)



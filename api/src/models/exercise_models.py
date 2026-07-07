from api.src.models.base_models import BaseOrmModel
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from api.src.utils.constraints import DatabaseConstraints

@BaseOrmModel.registry.mapped_as_dataclass
class Exercise:
    __tablename__ = "exercise"
    ___table_args__ = (UniqueConstraint("exercise_name", "user_id", name=DatabaseConstraints.Exercise.UNIQUE),)

    exercise_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id", name=DatabaseConstraints.Exercise.FK_USER), nullable=True
    )
    exercise_name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column(default=None, nullable=True)
    deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False, init=False)
    deleted_at: Mapped[datetime] = mapped_column(default=None, nullable=True)
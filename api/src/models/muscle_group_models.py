from api.src.models.base_models import BaseOrmModel
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

@BaseOrmModel.registry.mapped_as_dataclass
class MuscleGroup:
    __tablename__ = "muscle_group"

    user_id: Mapped[int] = mapped_column()
    group_name: Mapped[str] = mapped_column(primary_key=True)
    deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False, init=False)
    deleted_at: Mapped[datetime] = mapped_column(default=None, nullable=True)
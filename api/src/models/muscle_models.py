
from datetime import datetime

from sqlalchemy import ForeignKey, UniqueConstraint

from api.src.models.base_models import BaseOrmModel
from sqlalchemy.orm import Mapped, mapped_column

from api.src.utils.constraints import DatabaseConstraints


@BaseOrmModel.registry.mapped_as_dataclass
class Muscle:
    __tablename__ = "muscle"
    __table_args__ = (
        UniqueConstraint("muscle_name", "group_name", name=DatabaseConstraints.Muscle.UNIQUE)
    )

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    group_name: Mapped[str] = mapped_column(
        ForeignKey("muscle_group.group_name", name=DatabaseConstraints.Muscle.FK_MUSCLE_GROUP)
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id", name=DatabaseConstraints.Muscle.FK_USER),
        nullable=True
    )
    muscle_name: Mapped[str] = mapped_column()
    deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False, init=False)
    deleted_at: Mapped[datetime] = mapped_column(default=None, nullable=True)
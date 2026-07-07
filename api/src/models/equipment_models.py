from api.src.models.base_models import BaseOrmModel
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Index, UniqueConstraint
from api.src.utils.constraints import DatabaseConstraints
from datetime import datetime

@BaseOrmModel.registry.mapped_as_dataclass
class Equipment:
    __tablename__ = "equipment"
    __table_args__ = (
        UniqueConstraint("equipment_name", "user_id", name=DatabaseConstraints.Equipment.UNIQUE),
        Index(DatabaseConstraints.Equipment.IDX_EQUIPMENT_NAME, "equipment_name"),
    )

    equipment_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id", name=DatabaseConstraints.Equipment.FK_USER), nullable=True
    )
    group_name: Mapped[str] = mapped_column(
        ForeignKey("muscle_group.group_name", name=DatabaseConstraints.Equipment.FK_MUSCLE_GROUP)
        )
    equipment_name: Mapped[str] = mapped_column()
    deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False, init=False)
    deleted_at: Mapped[datetime] = mapped_column(default=None, nullable=True)

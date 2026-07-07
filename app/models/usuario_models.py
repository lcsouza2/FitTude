from datetime import datetime

from base_models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

@BaseModel.registry.mapped_as_dataclass
class User:
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True, init=False)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    deleted: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False, init=False)
    deleted_at: Mapped[datetime] = mapped_column(default=None, nullable=True)
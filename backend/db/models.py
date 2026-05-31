from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from db.base import ModelBase


class TaskOrm(ModelBase):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    short_link: Mapped[str] = mapped_column(unique=True)
    url: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime | None] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime | None] = mapped_column(
        default=datetime.now,
        onupdate=datetime.now,
    )
    is_active: Mapped[bool]
    is_deleted: Mapped[bool]

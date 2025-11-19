import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, Mapped

from .utils import get_datetime

class TimestampMixin:
    """Mixin to add created_at and updated_at timestamp columns to a SQLAlchemy model."""
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        default=get_datetime,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        default=get_datetime,
    )

class RecordMixin:
    """Mixin to add an auto-incrementing primary key 'id' column to a SQLAlchemy model."""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


__all__ = [
    "TimestampMixin",
    "RecordMixin",
]
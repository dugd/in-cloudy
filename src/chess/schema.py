from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint

from src.database.base import Base
from src.database.base_mixins import RecordMixin, TimestampMixin
from .config import GameTypes


class UserProfile(Base, RecordMixin, TimestampMixin):
    """SQLAlchemy model for chess user profiles."""
    __tablename__ = "user_profiles"

    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    profile_url: Mapped[str] = mapped_column(String(255), unique=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(255))

    stats: Mapped[List["UserStats"]] = relationship(back_populates="profile")


class UserStats(Base, RecordMixin, TimestampMixin):
    """SQLAlchemy model for chess user statistics."""
    __tablename__ = "user_stats"
    __table_args__ = (
        UniqueConstraint("profile_id", "game_type"),
    )

    game_type: Mapped[GameTypes] = mapped_column(String(50), nullable=False)
    games_played: Mapped[int] = mapped_column(Integer, default=0)
    games_won: Mapped[int] = mapped_column(Integer, default=0)
    highest_rating: Mapped[Optional[int]] = mapped_column(Integer)
    current_rating: Mapped[Optional[int]] = mapped_column(Integer)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profiles.id"))

    profile: Mapped["UserProfile"] = relationship(back_populates="stats")


__all__ = [
    "UserStats",
    "UserProfile",
]

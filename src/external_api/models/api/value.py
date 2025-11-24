from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional


class RatingEntry(BaseModel):
    rating: int
    date: Optional[datetime] = None
    rd: Optional[int] = None
    game: Optional[str] = None

    @validator("date", pre=True, always=True)
    def _parse_date(cls, v):
        if v is None or v == 0:
            return None
        if isinstance(v, datetime):
            return v
        try:
            # очікуємо ціле число UNIX timestamp (секунди)
            return datetime.fromtimestamp(int(v))
        except Exception as e:
            raise ValueError("date must be unix timestamp (int) or datetime") from e


class Record(BaseModel):
    win: int = 0
    loss: int = 0
    draw: int = 0
    time_per_move: Optional[int] = None
    timeout_percent: Optional[float] = None


class ModeStats(BaseModel):
    last: Optional[RatingEntry] = None
    best: Optional[RatingEntry] = None
    record: Optional[Record] = None


class TacticScore(BaseModel):
    rating: int
    date: Optional[datetime] = None

    @validator("date", pre=True, always=True)
    def _parse_date(cls, v):
        if v is None or v == 0:
            return None
        if isinstance(v, datetime):
            return v
        try:
            return datetime.fromtimestamp(int(v))
        except Exception as e:
            raise ValueError("date must be unix timestamp (int) or datetime") from e


class Tactics(BaseModel):
    highest: Optional[TacticScore] = None
    lowest: Optional[TacticScore] = None


class PuzzleRushScore(BaseModel):
    total_attempts: int
    score: int


class PuzzleRush(BaseModel):
    best: Optional[PuzzleRushScore] = None
    daily: Optional[PuzzleRushScore] = None

from typing import Literal, Optional
from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl

from .value import ModeStats, PuzzleRush, Tactics

ChessTimeClass = Literal["bullet", "blitz", "rapid", "daily"]


# for: https://api.chess.com/pub/player/{username}
class PlayerProfileAPI(BaseModel):
    """API response for player profile."""
    player_id: int
    url: HttpUrl
    username: str
    name: Optional[str] = None
    title: Optional[str] = None # GM, IM, etc
    country: Optional[HttpUrl] = Field(
        default=None,
    )
    location: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    followers: int = 0
    joined: Optional[datetime] = None
    last_online: Optional[datetime] = None
    is_streamer: bool = False
    twitch_url: Optional[HttpUrl] = None
    fide: Optional[int] = None

    status: str = None # basic | premium | staff | closed


# for: https://api.chess.com/pub/titled/{title-abbrev}
class TitlePlayersListAPI(BaseModel):
    """API response for a list of players with a specific title."""
    players: list[str]


# for: https://api.chess.com/pub/player/{username}/stats
class PlayerStatsAPI(BaseModel):
    chess_daily: Optional[ModeStats] = Field(None, alias="chess_daily")
    chess960_daily: Optional[ModeStats] = Field(None, alias="chess960_daily")
    chess_rapid: Optional[ModeStats] = Field(None, alias="chess_rapid")
    chess_bullet: Optional[ModeStats] = Field(None, alias="chess_bullet")
    chess_blitz: Optional[ModeStats] = Field(None, alias="chess_blitz")
    fide: Optional[int] = None
    tactics: Optional[Tactics] = None
    puzzle_rush: Optional[PuzzleRush] = Field(None, alias="puzzle_rush")

class Config:
    allow_population_by_field_name = True
    allow_population_by_alias = True
    extra = "ignore"
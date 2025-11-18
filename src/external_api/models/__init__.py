from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, Field, HttpUrl

if TYPE_CHECKING:
    from .api import PlayerProfileAPI, PlayerStatsAPI
    from .api.value import ModeStats, Record

class PlayerModeRecord(BaseModel):
    """A player's record in a specific game mode."""
    current_rating: int = Field(description="Current rating in this mode.")
    best_rating: int = Field(description="Highest rating achieved in this mode.")

    wins: int = Field(0, description="Number of wins in this mode.")
    losses: int = Field(0, description="Number of losses in this mode.")
    draws: int = Field(0, description="Number of draws in this mode.")

    @classmethod
    def from_mod_stats(cls, stats: Optional["ModeStats"]) -> "PlayerModeRecord":
        if stats is None or stats.last is None:
            return cls(
                current_rating=0,
                best_rating=0,
                wins=0,
                losses=0,
                draws=0,
            )
        record = stats.record or Record()
        best_rating = stats.best.rating if stats.best else stats.last.rating
        return cls(
            current_rating=stats.last.rating,
            best_rating=best_rating,
            wins=record.win,
            losses=record.loss,
            draws=record.draw,
        )

class PlayerSummary(BaseModel):
    """A summary of the player across all game modes."""
    username: str
    name: Optional[str] = Field(None, description="Real name or full name.")
    title: Optional[str] = Field(None, description="Player title, e.g. GM, IM, etc.")
    status: str = Field(
        None,
        description="Player status, e.g. basic, premium, staff, closed.",
    )

    profile_url: HttpUrl = Field(
        ...,
        description="Player's profile URL on chess.com.",
    )
    avatar_url: Optional[HttpUrl] = Field(
        None,
        description="Player's avatar URL.",
    )

    fide_rating: Optional[int] = Field(
        None,
        description="Player's FIDE rating, if available.",
    )
    followers: int = Field(
        0,
        description="Number of players' followers on chess.com.",
    )

    daily: PlayerModeRecord = Field(..., description="Daily Chess Statistics.")
    rapid: PlayerModeRecord = Field(..., description="Rapid Chess Statistics.")
    blitz: PlayerModeRecord = Field(..., description="Blitz Chess Statistics.")
    bullet: PlayerModeRecord = Field(..., description="Bullet Chess Statistics.")

    best_puzzle_rush_score: Optional[int] = Field(
        None, description="Best Puzzle Rush Score."
    )
    highest_tactic_rating: Optional[int] = Field(
        None, description="Highest tactic rating achieved."
    )

    @classmethod
    def from_api_data(cls, profile: "PlayerProfileAPI", stats: "PlayerStatsAPI") -> "PlayerSummary":
        daily_record = PlayerModeRecord.from_mod_stats(stats.chess_daily)
        rapid_record = PlayerModeRecord.from_mod_stats(stats.chess_rapid)
        blitz_record = PlayerModeRecord.from_mod_stats(stats.chess_blitz)
        bullet_record = PlayerModeRecord.from_mod_stats(stats.chess_bullet)

        best_puzzle_rush = (
            stats.puzzle_rush.best.score if stats.puzzle_rush and stats.puzzle_rush.best else None
        )
        highest_tactic = (
            stats.tactics.highest.rating if stats.tactics and stats.tactics.highest else None
        )

        return cls(
            username=profile.username,
            name=profile.name,
            title=profile.title,
            status=profile.status,
            profile_url=profile.url,
            avatar_url=profile.avatar,
            fide_rating=profile.fide,
            followers=profile.followers,
            daily=daily_record,
            rapid=rapid_record,
            blitz=blitz_record,
            bullet=bullet_record,
            best_puzzle_rush_score=best_puzzle_rush,
            highest_tactic_rating=highest_tactic,
        )
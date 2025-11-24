from .config import GameTypes
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_serializer
from src.database.base_schema import BaseOutSchema
from typing import Optional


class UserProfileCreate(BaseModel):
    username: str = Field(
        ...,
        description="Unique username for the chess user",
    )

    name: str = Field(
        ...,
        description="Full name of the chess user",
    )

    profile_url: HttpUrl = Field(
        ...,
        description="URL to the user's chess profile",
    )

    avatar_url: Optional[HttpUrl] = Field(
        None,
        description="URL to the user's avatar image",
    )

    @field_serializer("profile_url", "avatar_url")
    def _serialize_url(self, url, _info):
        return str(url)


class UserProfileUpdate(BaseModel):
    username: Optional[str] = Field(
        None,
        description="Unique username for the chess user",
    )

    name: Optional[str] = Field(
        None,
        description="Full name of the chess user",
    )

    profile_url: HttpUrl = Field(
        None,
        description="URL to the user's chess profile",
    )

    avatar_url: Optional[HttpUrl] = Field(
        None,
        description="URL to the user's avatar image",
    )


class UserProfileOut(BaseOutSchema):
    username: str = Field(
        ...,
        description="Unique username for the chess user",
    )

    name: str = Field(
        ...,
        description="Full name of the chess user",
    )

    profile_url: HttpUrl = Field(
        ...,
        description="URL to the user's chess profile",
    )

    avatar_url: Optional[HttpUrl] = Field(
        None,
        description="URL to the user's avatar image",
    )

    model_config = ConfigDict(from_attributes=True)


class UserProfileFullOut(UserProfileOut):
    """DTO for returning full user profile with statistics."""

    stats: list["UserStatsOut"] = Field(
        [],
        description="List of user statistics for different game types",
    )

    model_config = ConfigDict(from_attributes=True)


class UserStatsOut(BaseOutSchema):
    """DTO for returning statistics for a local cat fact."""

    game_type: GameTypes = Field(
        ...,
        description="Type of chess game (e.g., blitz, bullet, rapid)",
    )
    games_played: int = Field(
        0,
        description="Total number of games played",
    )
    games_won: int = Field(
        0,
        description="Total number of games won",
    )
    highest_rating: Optional[int] = Field(
        None,
        description="Highest rating achieved in this game type",
    )
    current_rating: Optional[int] = Field(
        None,
        description="Current rating in this game type",
    )
    profile_id: int = Field(
        ...,
        description="ID of the associated user profile",
    )

    model_config = ConfigDict(from_attributes=True)


__all__ = [
    "UserProfileCreate",
    "UserProfileUpdate",
    "UserProfileOut",
    "UserProfileFullOut",
    "UserStatsOut",
]

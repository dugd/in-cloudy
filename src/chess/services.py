from typing import Optional, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from .config import GameTypes, K_FACTOR
from .models import UserProfileOut, UserProfileFullOut, UserProfileCreate, UserStatsOut
from .repositories import UserProfileRepository, UserStatsRepository


class UserProfileService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.profile_repository = UserProfileRepository(session)

    async def create_user_profile(self, profile_data: UserProfileCreate) -> UserProfileOut:
        """Create a new user profile in the database."""

        profile = await self.profile_repository.create(profile_data.model_dump())
        return UserProfileOut.model_validate(profile)

    async def get_user_profile_by_username(self, profile_username: str) -> Optional[UserProfileOut]:
        """Retrieve a user profile by username."""

        profile = await self.profile_repository.get_by_username(profile_username)
        if profile is None:
            return None
        return UserProfileOut.model_validate(profile)

    async def get_random_user_profile(self) -> Optional[UserProfileOut]:
        """Retrieve a random user profile if available."""

        profile = await self.profile_repository.get_random()
        if profile is None:
            return None
        return UserProfileOut.model_validate(profile)

    async def get_full_user_profile(self, profile_id: int) -> Optional[UserProfileFullOut]:
        """Retrieve a user profile along with associated statistics by id."""

        profile = await self.profile_repository.get_with_stats(profile_id)
        if profile is None:
            return None
        return UserProfileFullOut.model_validate(profile)


class UserStatsService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.stats_repository = UserStatsRepository(session)

    async def get_user_stats(self, profile_id: int) -> Sequence[UserStatsOut]:
        """Retrieve all statistics for a given user by user ID."""

        stats = await self.stats_repository.get_by_profile_id(profile_id)
        return [UserStatsOut.model_validate(stat) for stat in stats]

    async def get_user_stats_by_game_type(self, profile_id: int, game_type: GameTypes) -> Optional[UserStatsOut]:
        """Retrieve statistics for a given user by user ID and game type."""

        stat = await self.stats_repository.get_by_profile_and_game_type(profile_id, game_type)
        if stat is None:
            return None
        return UserStatsOut.model_validate(stat)


class PlayGameService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.profile_repository = UserProfileRepository(session)
        self.stats_repository = UserStatsRepository(session)

    @staticmethod
    async def _calculate_elo_change(rating1: int, rating2: int, result: bool) -> tuple[int, int]:
        """Calculate the ELO rating change for two players based on the game result."""
        k = K_FACTOR  # K-factor in ELO calculation

        expected_score1 = 1 / (1 + 10 ** ((rating2 - rating1) / 400))
        expected_score2 = 1 / (1 + 10 ** ((rating1 - rating2) / 400))

        actual_score1 = 1.0 if result else 0.0
        actual_score2 = 0.0 if result else 1.0

        new_rating1 = rating1 + k * (actual_score1 - expected_score1)
        new_rating2 = rating2 + k * (actual_score2 - expected_score2)

        return int(round(new_rating1)), int(round(new_rating2))

    async def record_game_result(self, profile1_id: int, profile2_id, game_type: GameTypes, result: bool) -> Optional[tuple[UserStatsOut, UserStatsOut]]:
        """Record the result of a game between two users and update their statistics."""

        if not await self.profile_repository.exists(profile1_id) or not await self.profile_repository.exists(profile2_id):
            return None

        profile1_stats = await self.stats_repository.get_by_profile_and_game_type(profile1_id, game_type)
        profile2_stats = await self.stats_repository.get_by_profile_and_game_type(profile2_id, game_type)

        if profile1_stats is None:
            profile1_stats = await self.stats_repository.create_by_default(profile1_id, game_type)
        if profile2_stats is None:
            profile2_stats = await self.stats_repository.create_by_default(profile2_id, game_type)

        rating1 = profile1_stats.current_rating or 1200
        rating2 = profile2_stats.current_rating or 1200

        new_rating1, new_rating2 = await self._calculate_elo_change(rating1, rating2, result)

        profile1_stats.current_rating = new_rating1
        profile2_stats.current_rating = new_rating2

        if profile1_stats.highest_rating is None or new_rating1 > profile1_stats.highest_rating:
            profile1_stats.highest_rating = new_rating1
        if profile2_stats.highest_rating is None or new_rating2 > profile2_stats.highest_rating:
            profile2_stats.highest_rating = new_rating2

        if result:
            profile1_stats.games_won += 1
        else:
            profile2_stats.games_won += 1

        profile1_stats.games_played += 1
        profile2_stats.games_played += 1

        await self.session.commit()

        await self.session.refresh(profile1_stats)
        await self.session.refresh(profile2_stats)

        return UserStatsOut.model_validate(profile1_stats), UserStatsOut.model_validate(profile2_stats)
from .config import GameTypes
from .schema import UserProfile, UserStats
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from src.database.base_repository import BaseRepository
from typing import List, Optional, Sequence


class UserProfileRepository(BaseRepository[UserProfile]):
    """Repository for managing user profiles in the database."""

    def __init__(self, session: AsyncSession):
        super().__init__(UserProfile, session)

    async def get_random(self) -> Optional[UserProfile]:
        """Retrieve a random user profile from the database."""
        stmt = select(UserProfile).order_by(func.random()).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> Optional[UserProfile]:
        """Retrieve a user profile by username."""
        stmt = select(UserProfile).where(UserProfile.username == username)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_with_stats(self, profile_id: int) -> Optional[UserProfile]:
        """Retrieve a user profile along with associated statistics by id."""
        stmt = select(UserProfile).options(selectinload(UserProfile.stats)).where(UserProfile.id == profile_id)

        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists(self, profile_id: int) -> bool:
        """Check if a user profile exists by ID."""
        stmt = select(func.count()).select_from(UserProfile).where(UserProfile.id == profile_id)
        result = await self.session.execute(stmt)
        count = result.scalar_one()
        return count > 0


class UserStatsRepository(BaseRepository[UserStats]):
    """Repository for managing user statistics in the database."""

    def __init__(self, session: AsyncSession):
        super().__init__(UserStats, session)

    async def get_by_profile_id(self, profile_id: int) -> Sequence[UserStats]:
        """Retrieve all statistics for a given user by user ID."""
        stmt = select(UserStats).where(UserStats.profile_id == profile_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_profile_and_game_type(self, profile_id: int, game_type: GameTypes) -> Optional[UserStats]:
        """Retrieve statistics for a given user by user ID and game type."""
        stmt = select(UserStats).where(UserStats.profile_id == profile_id, UserStats.game_type == game_type)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_by_default_all(self, profile_id: int) -> List[UserStats]:
        """Create default statistics entries for a new user profile."""
        game_types: List[GameTypes] = [game_type for game_type in GameTypes]
        stats_entries = [
            UserStats(profile_id=profile_id, game_type=game_type, games_played=0, games_won=0)
            for game_type in game_types
        ]
        self.session.add_all(stats_entries)
        await self.session.commit()
        await self.session.refresh(stats_entries)

        return stats_entries

    async def create_by_default(self, profile_id: int, game_type: GameTypes) -> UserStats:
        """Create a default statistics entry for a new user profile and game type."""
        stats_entry = UserStats(profile_id=profile_id, game_type=game_type, games_played=0, games_won=0)
        self.session.add(stats_entry)
        await self.session.commit()
        await self.session.refresh(stats_entry)

        return stats_entry

    @staticmethod
    async def _update_stats_rating(stats: UserStats, new_rating: int) -> UserStats:
        """Helper method to update the rating in user statistics."""
        stats.current_rating = new_rating
        if stats.highest_rating is None or new_rating > stats.highest_rating:
            stats.highest_rating = new_rating
        return stats

    async def increment_games_played(
        self, profile_id: int, game_type: GameTypes, new_rating: int
    ) -> Optional[UserStats]:
        """Increment the games played count for a user's statistics. (counts as losing a game)"""
        stmt = select(UserStats).where(UserStats.profile_id == profile_id, UserStats.game_type == game_type)
        result = await self.session.execute(stmt)
        stats = result.scalar_one_or_none()

        if stats:
            stats.games_played += 1

            await self._update_stats_rating(stats, new_rating)

            self.session.add(stats)
            await self.session.commit()
            await self.session.refresh(stats)

        return stats

    async def increment_games_won(self, profile_id: int, game_type: GameTypes, new_rating: int) -> Optional[UserStats]:
        """Increment the games won count for a user's statistics."""
        stmt = select(UserStats).where(UserStats.profile_id == profile_id, UserStats.game_type == game_type)
        result = await self.session.execute(stmt)
        stats = result.scalar_one_or_none()

        if stats:
            stats.games_won += 1
            stats.games_played += 1  # also counts as a played game

            await self._update_stats_rating(stats, new_rating)

            self.session.add(stats)
            await self.session.commit()
            await self.session.refresh(stats)

        return stats

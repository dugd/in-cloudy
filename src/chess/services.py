from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .models import UserProfileOut, UserProfileFullOut, UserProfileCreate
from .repositories import UserProfileRepository


class UserProfileService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.profile_repository = UserProfileRepository(session)

    async def create_user_profile(self, profile_data: UserProfileCreate) -> UserProfileOut:
        """Create a new user profile in the database."""

        profile = await self.profile_repository.create(profile_data.model_dump())
        return UserProfileOut.model_validate(profile)

    async def get_user_profile(self, profile_username: str) -> Optional[UserProfileOut]:
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

    async def get_full_user_profile(self, profile_username: str) -> Optional[UserProfileFullOut]:
        """Retrieve a user profile along with associated statistics by username."""

        profile = await self.profile_repository.get_with_stats(profile_username)
        if profile is None:
            return None
        return UserProfileFullOut.model_validate(profile)

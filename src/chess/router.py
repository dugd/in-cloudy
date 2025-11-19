from fastapi import APIRouter, Depends
from src.database.context import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from .services import UserProfileService
from .models import UserProfileOut, UserProfileCreate, UserProfileFullOut

router = APIRouter(prefix="/chess", tags=["chess"])


def get_profile_service(session: AsyncSession = Depends(get_db_session)) -> UserProfileService:
    return UserProfileService(session)

# --- User Profile Endpoints ---

@router.post("/profiles", summary="Create a new user profile", response_model=UserProfileOut)
async def create_user_profile(
    profile_data: UserProfileCreate,
    profile_service: UserProfileService = Depends(get_profile_service),
):
    profile = await profile_service.create_user_profile(profile_data)
    return profile

@router.get("/profiles/{username}", summary="Get a user profile by username", response_model=UserProfileOut)
async def get_user_profile(
    username: str,
    profile_service: UserProfileService = Depends(get_profile_service),
):
    profile = await profile_service.get_user_profile(username)
    return profile

@router.get("/profiles/random", summary="Get a random user profile", response_model=UserProfileOut)
async def get_random_user_profile(
    profile_service: UserProfileService = Depends(get_profile_service),
):
    profile = await profile_service.get_random_user_profile()
    return profile

@router.get("/profiles/{username}/full", summary="Get a full user profile with stats by username", response_model=UserProfileFullOut)
async def get_full_user_profile(
    username: str,
    profile_service: UserProfileService = Depends(get_profile_service),
):
    profile = await profile_service.get_full_user_profile(username)
    return profile

# --- Additional endpoints can be added here ---

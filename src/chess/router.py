from fastapi import APIRouter, Depends, HTTPException
from src.database.context import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from .services import UserProfileService, UserStatsService, PlayGameService
from .models import UserProfileOut, UserProfileCreate, UserProfileFullOut, UserStatsOut
from .config import GameTypes

router = APIRouter(prefix="/chess", tags=["chess"])


def get_profile_service(session: AsyncSession = Depends(get_db_session)) -> UserProfileService:
    return UserProfileService(session)

def get_stats_service(session: AsyncSession = Depends(get_db_session)) -> UserStatsService:
    return UserStatsService(session)

def get_play_game_service(session: AsyncSession = Depends(get_db_session)) -> PlayGameService:
    return PlayGameService(session)

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
    profile = await profile_service.get_user_profile_by_username(username)
    if profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

@router.get("/profiles/random", summary="Get a random user profile", response_model=UserProfileOut)
async def get_random_user_profile(
    profile_service: UserProfileService = Depends(get_profile_service),
):
    profile = await profile_service.get_random_user_profile()
    if profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

@router.get("/profiles/{profile_id}/full", summary="Get a full user profile with stats by id", response_model=UserProfileFullOut)
async def get_full_user_profile(
    profile_id: int,
    profile_service: UserProfileService = Depends(get_profile_service),
):
    profile = await profile_service.get_full_user_profile(profile_id)
    if profile is None:
        raise HTTPException(status_code=404, detail="User profile not found")
    return profile

# --- User Stats Endpoints ---

@router.get("/profiles/{profile_id}/stats", summary="Get all user stats by profile id", response_model=list[UserStatsOut])
async def get_user_stats(
    profile_id: int,
    stats_service: UserStatsService = Depends(get_stats_service),
):
    stats = await stats_service.get_user_stats(profile_id)
    if stats is None:
        raise HTTPException(status_code=404, detail="User stats not found")
    return stats

@router.get("/profiles/{profile_id}/stats/{game_type}", summary="Get user stats by profile id and game type", response_model=UserStatsOut)
async def get_user_stats_by_game_type(
    profile_id: int,
    game_type: GameTypes,
    stats_service: UserStatsService = Depends(get_stats_service),
):
    stats = await stats_service.get_user_stats_by_game_type(profile_id, game_type)
    if stats is None:
        raise HTTPException(status_code=404, detail="User stats not found")
    return stats

# --- Play Game Endpoint ---

@router.post("/record", summary="Record the result of a game between two players")
async def record_result(
    player_id: int,
    opponent_id: int,
    game_type: GameTypes,
    won: bool,
    play_game_service: PlayGameService = Depends(get_play_game_service),
):
    result = await play_game_service.record_game_result(player_id, opponent_id, game_type, won)
    if result is None:
        raise HTTPException(status_code=404, detail="One or both user profiles not found")
    return result

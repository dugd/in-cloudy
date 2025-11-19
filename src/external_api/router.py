from fastapi import APIRouter, HTTPException

from .models import PlayerSummary
from .models.api import PlayerStatsAPI, PlayerProfileAPI
from .service import service


router = APIRouter(prefix="/external-api", tags=["external-api"])


@router.get("/profile", response_model=PlayerProfileAPI)
async def get_profile(username: str):
    try:
        profile = service.get_player_profile(username)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=PlayerStatsAPI)
async def get_stats(username: str):
    try:
        stats = service.get_player_stats(username)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary", response_model=PlayerSummary)
async def get_summary(username: str):
    try:
        summary = service.get_player_summary(username)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users-by-title", response_model=list[str])
async def get_users_by_title(title_abbrev: str):
    try:
        users = service.get_users_by_title(title_abbrev)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
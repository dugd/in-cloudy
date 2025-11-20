from fastapi import APIRouter, HTTPException, Depends
import aiohttp

from src.cache import get_cache_service, CacheService
from .models import PlayerSummary
from .models.api import PlayerStatsAPI, PlayerProfileAPI
from .service import ChessService


router = APIRouter(prefix="/external-api", tags=["external-api"])


async def get_http_client():
    async with aiohttp.ClientSession() as session:
        yield session


async def get_service(
        cache: CacheService = Depends(get_cache_service),
        client: aiohttp.ClientSession = Depends(get_http_client),
) -> ChessService:
    return ChessService(client, cache)


@router.get("/profile", response_model=PlayerProfileAPI)
async def get_profile(username: str, service: ChessService = Depends(get_service)):
    try:
        profile = await service.get_player_profile(username)
        return profile
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stats", response_model=PlayerStatsAPI)
async def get_stats(username: str, service: ChessService = Depends(get_service)):
    try:
        stats = await service.get_player_stats(username)
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary", response_model=PlayerSummary)
async def get_summary(username: str, service: ChessService = Depends(get_service)):
    try:
        summary = await service.get_player_summary(username)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/users-by-title", response_model=list[str])
async def get_users_by_title(title_abbrev: str, service: ChessService = Depends(get_service)):
    try:
        users = await service.get_users_by_title(title_abbrev)
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
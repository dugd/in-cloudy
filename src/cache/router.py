from .deps import get_cache_service
from .models import CacheItem
from .service import CacheService
from fastapi import APIRouter, Depends, HTTPException

router = APIRouter(prefix="/cache", tags=["cache"])


@router.post("/set", summary="Set a value in the cache")
async def set_cache_item(item: CacheItem, cache_service: CacheService = Depends(get_cache_service)):
    await cache_service.cache_set(item.key, item.value, ttl=item.ttl)
    return {"status": "saved", "key": item.key}


@router.get("/get/{key}", summary="Get a value from the cache")
async def get_cache_item(key: str, cache_service: CacheService = Depends(get_cache_service)):
    value = await cache_service.cache_get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found") from None

    return {"key": key, "value": value}

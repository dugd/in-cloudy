from fastapi import Request
import redis.asyncio as redis

from .service import CacheService


async def get_redis(request: Request) -> redis.Redis:
    return request.app.state.redis

async def get_cache_service(request: Request) -> "CacheService":
    redis_client = await get_redis(request)
    return CacheService(redis_client)

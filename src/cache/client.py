from redis import asyncio as aioredis
from .config import redis_config


def init_redis() -> aioredis.Redis:
    return aioredis.from_url(
        redis_config.URL,
        encoding="utf-8",
        decode_responses=True,
    )

import json


class CacheService:
    def __init__(self, redis_client):
        self.redis = redis_client

    async def cache_set(self, key: str, value, ttl: int | None = None):
        await self.redis.set(key, json.dumps(value), ex=ttl)


    async def cache_get(self, key: str):
        data = await self.redis.get(key)
        return json.loads(data) if data else None

from .router import router as cache_router
from .client import init_redis
from .deps import get_redis, get_cache_service
from .service import CacheService

import aiohttp

from src.cache import CacheService
from .models import PlayerSummary
from .models.api import PlayerStatsAPI, PlayerProfileAPI, TitlePlayersListAPI
from .config import chess_com_config

class ChessService:
    """Service class for handling chess game data."""

    api_url = chess_com_config.api_base_url
    url = chess_com_config.web_base_url

    default_headers = {
        "Host": chess_com_config.api_host,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
    }

    def __init__(self, client: aiohttp.ClientSession, cache: CacheService):
        self.client = client
        self.client.headers.update(self.default_headers)
        self.cache = cache

    async def get_player_profile(self, username) -> PlayerProfileAPI:
        """Fetches the profile of a chess player by username."""

        cache_key = f"player_profile:{username}"
        cached_profile = await self.cache.cache_get(cache_key)
        if cached_profile:
            return PlayerProfileAPI(**cached_profile)

        response = await self.client.get(f"{self.api_url}/pub/player/{username}")
        response.raise_for_status()

        data = await response.json()
        await self.cache.cache_set(cache_key, data, ttl=chess_com_config.cache_ttl)  # Cache

        return PlayerProfileAPI(**data)

    async def get_player_stats(self, username) -> PlayerStatsAPI:
        """Fetches the statistics of a chess player by username."""

        cache_key = f"player_stats:{username}"
        cached_stats = await self.cache.cache_get(cache_key)
        if cached_stats:
            return PlayerStatsAPI(**cached_stats)

        response = await self.client.get(f"{self.api_url}/pub/player/{username}/stats")
        response.raise_for_status()

        data = await response.json()
        await self.cache.cache_set(
            cache_key, data, ttl=chess_com_config.cache_ttl
        )  # Cache

        return PlayerStatsAPI(**data)

    async def get_player_summary(self, username) -> PlayerSummary:
        """Fetches the summary of a chess player by username."""

        profile = await self.get_player_profile(username)
        stats = await self.get_player_stats(username)

        return PlayerSummary.from_api_data(profile=profile, stats=stats)

    async def get_users_by_title(self, title_abbrev: str) -> list[str]:
        """Fetches a list of usernames with a specific chess title."""

        response = await self.client.get(f"{self.api_url}/pub/titled/{title_abbrev}")
        response.raise_for_status()
        return TitlePlayersListAPI(**await response.json()).players

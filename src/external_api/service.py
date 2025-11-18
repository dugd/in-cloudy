from typing import Optional

import requests

from .models import PlayerSummary
from .models.api import PlayerStatsAPI, PlayerProfileAPI

class ChessService:
    """Service class for handling chess game data."""

    api_url = "https://api.chess.com/"
    url = "https://www.chess.com/"

    def get_player_profile(self, username) -> Optional[PlayerProfileAPI]:
        """Fetches the profile of a chess player by username."""
        response = requests.get(f"{self.api_url}pub/player/{username}")
        if response.status_code == 200:
            return PlayerProfileAPI(**response.json())
        return None

    def get_player_stats(self, username) -> Optional[PlayerStatsAPI]:
        """Fetches the statistics of a chess player by username."""
        response = requests.get(f"{self.api_url}pub/player/{username}/stats")
        if response.status_code == 200:
            return PlayerStatsAPI(**response.json())
        return None

    def get_player_summary(self, username) -> Optional[PlayerSummary]:
        """Fetches the summary of a chess player by username."""
        profile = self.get_player_profile(username)
        stats = self.get_player_stats(username)

        if not profile or not stats:
            return None

        return PlayerSummary.from_api_data(profile=profile, stats=stats)


service = ChessService()

from typing import Optional

import requests

from .models import PlayerSummary
from .models.api import PlayerStatsAPI, PlayerProfileAPI, ErrorAPI, TitlePlayersListAPI
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

    def __init__(self):
        self.session: Optional[requests.Session] = None

    def _init_session(self):
        if self.session is None:
            self.session = requests.Session()

    def _get_session(self) -> requests.Session:
        if self.session is None:
            self._init_session()
        return self.session

    def get_player_profile(self, username) -> PlayerProfileAPI:
        """Fetches the profile of a chess player by username."""
        response = requests.get(f"{self.api_url}/pub/player/{username}", headers=self.default_headers)
        response.raise_for_status()
        return PlayerProfileAPI(**response.json())

    def get_player_stats(self, username) -> PlayerStatsAPI:
        """Fetches the statistics of a chess player by username."""
        response = requests.get(f"{self.api_url}/pub/player/{username}/stats", headers=self.default_headers)
        response.raise_for_status()
        return PlayerStatsAPI(**response.json())

    def get_player_summary(self, username) -> PlayerSummary:
        """Fetches the summary of a chess player by username."""
        profile = self.get_player_profile(username)
        stats = self.get_player_stats(username)

        return PlayerSummary.from_api_data(profile=profile, stats=stats)

    def get_users_by_title(self, title_abbrev: str) -> list[str]:
        """Fetches a list of usernames with a specific chess title."""
        response = requests.get(f"{self.api_url}/pub/titled/{title_abbrev}", headers=self.default_headers)
        response.raise_for_status()
        return TitlePlayersListAPI(**response.json()).players


service = ChessService()

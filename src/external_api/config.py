from dataclasses import dataclass


@dataclass
class ChessComConfig:
    api_host: str = "api.chess.com"
    api_base_url: str = "https://api.chess.com"
    web_base_url: str = "https://www.chess.com"

    cache_ttl: int = 60


chess_com_config = ChessComConfig()

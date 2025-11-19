from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresConfig(BaseSettings):
    """Configuration settings for connecting to a PostgreSQL database."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PG_",
    )

    HOST: str
    PASSWORD: str
    PORT: int = 5432
    USERNAME: str
    DATABASE: str

    def postgres_uri(self, driver: Literal["asyncpg"] = "asyncpg") -> str:
        return f"postgresql+{driver}://{self.USERNAME}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"


postgres_config = PostgresConfig()

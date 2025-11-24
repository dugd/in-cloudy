from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class PostgresConfig(BaseSettings):
    """Configuration settings for connecting to a PostgreSQL database."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PG_",
        extra="ignore",
    )

    HOST: str
    PASSWORD: str
    PORT: int = 5432
    USER: str
    DATABASE: str

    def postgres_uri(self, driver: Literal["asyncpg"] = "asyncpg") -> str:
        return f"postgresql+{driver}://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}"


postgres_config = PostgresConfig()

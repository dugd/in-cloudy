
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisConfig(BaseSettings):
    """Configuration settings for connecting to a Redis cache."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="REDIS_",
        extra="ignore",
    )

    URL: str


redis_config = RedisConfig()

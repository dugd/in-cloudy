from pydantic_settings import BaseSettings, SettingsConfigDict


class SentryConfig(BaseSettings):
    """Configuration settings for connecting to Sentry error tracking service."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="SENTRY_",
        extra="ignore",
    )

    DSN: str

sentry_config = SentryConfig()

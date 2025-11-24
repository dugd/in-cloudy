"""Database connection setup using SQLAlchemy AsyncIO. Import to connect to the database."""

from .config import postgres_config
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(postgres_config.postgres_uri(), echo=False)

AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)


__all__ = [
    "engine",
    "AsyncSessionLocal",
]

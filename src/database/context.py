from .connect import AsyncSessionLocal


async def get_db_session():
    """FastAPI dependency: yields an async DB session."""
    async with AsyncSessionLocal() as session:
        yield session

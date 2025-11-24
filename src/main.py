from contextlib import asynccontextmanager

from fastapi import FastAPI
from alembic.config import Config
from alembic import command

from src.core import health_router
from src.cache import init_redis, cache_router
from src.storage import storage_router
from src.external_api import external_api_router
from src.chess import chess_router
from src.telemetry import init_telemetry

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


# run_migrations()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_telemetry()
    redis = init_redis()

    app.state.redis = redis

    try:
        await redis.ping()
    except Exception:
        raise

    yield

    await app.state.redis.aclose()


app = FastAPI(
    title="FastAPI Project",
    description="Lab project with FastAPI and Swagger UI",
    version="0.2.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(cache_router)
app.include_router(storage_router)
app.include_router(external_api_router)
app.include_router(chess_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Project!"}

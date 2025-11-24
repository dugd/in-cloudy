from alembic import command
from alembic.config import Config
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.cache import cache_router, init_redis
from src.chess import chess_router
from src.core import health_router
from src.external_api import external_api_router
from src.storage import storage_router
from src.telemetry import init_telemetry, setup_logging


def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


# run_migrations()


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
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

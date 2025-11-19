from fastapi import FastAPI
from src.core import health_router
from src.storage import storage_router
from src.external_api import external_api_router
from alembic.config import Config
from alembic import command

def run_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


run_migrations()


app = FastAPI(
    title="FastAPI Project",
    description="Lab project with FastAPI and Swagger UI",
    version="0.2.0",
)

app.include_router(health_router)
app.include_router(storage_router)
app.include_router(external_api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Project!"}

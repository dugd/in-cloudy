from fastapi import FastAPI
from src.core import health_router
from src.storage import storage_router

app = FastAPI(
    title="Lab3 FastAPI Project",
    description="Lab project with FastAPI and Swagger UI",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(storage_router)

import os

import pytest
from fastapi.testclient import TestClient
import fakeredis.aioredis

# Set a default Redis URL for testing purposes (Temporary fix)
os.environ.setdefault("REDIS_URL", "redis://localhost:6379/0")
os.environ.setdefault("PG_HOST", "localhost")
os.environ.setdefault("PG_PORT", "5432")
os.environ.setdefault("PG_DATABASE", "test_db")
os.environ.setdefault("PG_USER", "test_user")
os.environ.setdefault("PG_PASSWORD", "test_password")
os.environ.setdefault("SENTRY_DSN", "")

from src.main import app

os.environ["TESTING"] = "1"


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture
def fake_redis(monkeypatch):
    redis = fakeredis.aioredis.FakeRedis()

    monkeypatch.setattr("src.cache.deps.get_redis", lambda: redis)

    return redis

from functools import lru_cache

import pytest
from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    engine_url: str = "sqlite+pysqlite:///:memory:"


@lru_cache
def settings_test():
    settings = TestSettings()
    return settings


@pytest.fixture
def app_test():
    from app.main import app
    from app.core.dependencies import get_settings

    app.dependency_overrides[get_settings] = settings_test
    yield app
    app.dependency_overrides = {}


@pytest.fixture
def client(app_test):
    return TestClient(app_test)

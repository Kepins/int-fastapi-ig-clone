from functools import lru_cache

import pytest
from fastapi.testclient import TestClient

from app.core.settings import Settings


@lru_cache
def settings_test() -> Settings:
    return Settings(_env_file="test.env", _env_file_encoding="utf-8")


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

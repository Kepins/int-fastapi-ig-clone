from functools import lru_cache

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from app.core.dependencies import get_db
from app.core.settings import Settings
from app.db.models.base import Base


@lru_cache
def settings_test() -> Settings:
    return Settings(_env_file="test.env", _env_file_encoding="utf-8")


engine = create_engine(settings_test().engine_url)

db_session = scoped_session(sessionmaker(bind=engine))
Base.metadata.create_all(bind=engine)

db = db_session()


def get_db_test():
    try:
        yield db
    finally:
        db.rollback()


@pytest.fixture
def app_test():
    from app.main import app
    from app.core.dependencies import get_settings

    app.dependency_overrides[get_settings] = settings_test
    app.dependency_overrides[get_db] = get_db_test
    yield app
    app.dependency_overrides = {}


@pytest.fixture(scope="module")
def test_file_jpg():
    with open("tests/test_pictures/pict.jpg", mode="rb") as file:
        return "pict.jpg", file.read()

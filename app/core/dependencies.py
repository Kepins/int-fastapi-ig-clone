from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .settings import Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_db(settings: Annotated[Settings, Depends(get_settings)]) -> Session:
    get_db.sessions = getattr(get_db, "sessions", {})
    try:
        db_session = get_db.sessions[settings.engine_url]
    except KeyError as e:
        get_db.sessions[settings.engine_url] = scoped_session(
            sessionmaker(bind=create_engine(settings.engine_url))
        )
        db_session = get_db.sessions[settings.engine_url]

    try:
        db_session()
        yield db_session
    finally:
        db_session.remove()

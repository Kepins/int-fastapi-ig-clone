from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .settings import Settings
from ..services.user_service import get_user_by_id


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
        db_session.commit()
        db_session.remove()


def get_current_user(db: Annotated[Session, Depends(get_db)]):
    # TODO return authenticated user or raise HTTPException if does not exist
    return get_user_by_id(db, 4)

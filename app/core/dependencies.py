from functools import lru_cache
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from .settings import Settings
from ..repositories.file_repository import FileRepository
from ..services.user_service import get_user_by_id
from ..services.exceptions import NotFound

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/account/login")


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


def get_file_repository(settings: Annotated[Settings, Depends(get_settings)]) -> FileRepository:
    return FileRepository(directory=settings.FILE_DIRECTORY)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired Auth-Token"
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Auth-Token"
        )
    try:
        return get_user_by_id(db, payload["user_id"])
    except NotFound:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User Deleted"
        )

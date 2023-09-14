from functools import lru_cache
from typing import Annotated

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

app = FastAPI()

from .core.settings import Settings
@lru_cache
def get_settings():
    return Settings()


from .core.db import db_session
def get_db():
    try:
        db_session()
        yield db_session
    finally:
        db_session.remove()

@app.get("/")
async def root(db: Annotated[Session, Depends(get_db)]):
    return {"message": "Hello World!"}

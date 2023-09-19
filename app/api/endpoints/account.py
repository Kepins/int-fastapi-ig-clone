from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from ...core.dependencies import get_db
from ...routers.account import router


@router.put(path="", name="Update account")
def update(db: Annotated[Session, Depends(get_db)]):
    pass


@router.post(path="/login", name="Login")
def login(db: Annotated[Session, Depends(get_db)]):
    pass


@router.post(path="/reset_password", name="Reset account password")
def reset_password(db: Annotated[Session, Depends(get_db)]):
    pass


@router.delete(path="", name="Delete account")
def delete(db: Annotated[Session, Depends(get_db)]):
    pass

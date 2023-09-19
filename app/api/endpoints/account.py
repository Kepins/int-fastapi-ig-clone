from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from ...core.dependencies import get_db, get_current_user
from ...routers.account import router
from ...schemas.user import User, UserUpdate
from ...services.user_service import update_user


@router.put(path="", name="Update account")
def update(new_user: UserUpdate, user: Annotated[User, Depends(get_current_user)], db: Annotated[Session, Depends(get_db)]) -> User:
    return update_user(db, User(**(user.model_dump() | new_user.model_dump())))


@router.post(path="/login", name="Login")
def login(db: Annotated[Session, Depends(get_db)]):
    pass


@router.post(path="/reset_password", name="Reset account password")
def reset_password(db: Annotated[Session, Depends(get_db)]):
    pass


@router.delete(path="", name="Delete account")
def delete(db: Annotated[Session, Depends(get_db)]):
    pass

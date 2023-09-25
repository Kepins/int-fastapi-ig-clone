from typing import Annotated

from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from ...core.dependencies import get_db, get_current_user
from ...routers.account import router
from ...schemas.user import User, UserUpdate, UserResetPassword
from ...services import user_service
from ...services.exceptions import PasswordNotMatching


@router.put(path="", name="Update account")
def update(
    new_user: UserUpdate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    return user_service.update_user(
        db, User(**(user.model_dump() | new_user.model_dump()))
    )


@router.post(path="/login", name="Login")
def login(db: Annotated[Session, Depends(get_db)]):
    pass


@router.post(path="/reset_password", name="Reset account password")
def reset_password(
    passwords: UserResetPassword,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    try:
        user_service.reset_password(db, user, passwords)
    except PasswordNotMatching as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Password Not Valid"
        )


@router.delete(path="", name="Delete account", status_code=status.HTTP_204_NO_CONTENT)
def delete(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> None:
    user_service.delete_user_by_id(db, user.id)

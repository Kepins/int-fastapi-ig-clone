from typing import Annotated, List

from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session

from ...core.dependencies import get_db
from ...routers.users import router
from ...schemas.shared import HTTPError
from ...schemas.user import User, UserCreate
from ...services.exceptions import AlreadyExists, NotFound
from ...services import user_service


@router.get("/", name="Get all users")
def get_list(db: Annotated[Session, Depends(get_db)]) -> List[User]:
    return user_service.get_all_users(db)


@router.post(
    "/",
    name="Create user",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_409_CONFLICT: {"model": HTTPError}},
)
def create(user: UserCreate, db: Annotated[Session, Depends(get_db)]) -> User:
    try:
        return user_service.create_user(db, user)
    except AlreadyExists as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User Already Exists"
        )


@router.get(
    "/{id:int}",
    name="Get user",
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPError}},
)
def get(id: int, db: Annotated[Session, Depends(get_db)]) -> User:
    try:
        return user_service.get_user_by_id(db, id)
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found"
        )

from typing import Annotated

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import Response
from sqlalchemy.orm import Session

from ...core.dependencies import get_db, get_current_user, get_settings
from ...core.security import create_access_token
from ...core.settings import Settings
from ...routers.account import router
from ...schemas.shared import HTTPError
from ...schemas.user import User, UserUpdate, UserResetPassword
from ...services import user_service
from ...services.exceptions import PasswordNotMatching, NotFound


@router.get(
    "",
    name="Get account info",
    responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTPError}},
)
def account_info(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    return user


@router.put(
    path="",
    name="Update account",
    responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTPError}},
)
def update(
    new_user: UserUpdate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> User:
    return user_service.update_user(
        db, User(**(user.model_dump() | new_user.model_dump()))
    )


@router.post(
    path="/login",
    name="Login to account",
    responses={status.HTTP_400_BAD_REQUEST: {"model": HTTPError}},
)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    settings: Annotated[Settings, Depends(get_settings)],
    db: Annotated[Session, Depends(get_db)],
):
    nickname = form_data.username
    password = form_data.password

    httpexception = HTTPException(
        status_code=400, detail="Incorrect Username Or Password"
    )
    try:
        user = user_service.get_user_by_nickname(db, nickname)
    except NotFound:
        raise httpexception
    if not user_service.verify_password(db, user, password):
        raise httpexception

    return {"access_token": create_access_token(user, settings), "token_type": "bearer"}


@router.post(
    path="/reset_password",
    name="Reset account password",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": HTTPError},
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPError},
    },
)
def reset_password(
    passwords: UserResetPassword,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    try:
        user_service.reset_password(db, user, passwords)
        return Response(status_code=status.HTTP_200_OK)
    except PasswordNotMatching as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Password Not Valid"
        )


@router.delete(
    path="",
    name="Delete account",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_401_UNAUTHORIZED: {"model": HTTPError}},
)
def delete(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Response:
    user_service.delete_user_by_id(db, user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

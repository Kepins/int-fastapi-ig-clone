from typing import Annotated, List

from fastapi import Depends, UploadFile, Form, File, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ...core.dependencies import get_db, get_file_repository, get_current_user
from ...repositories.file_repository import FileRepository
from ...routers.photos import router
from ...schemas.photo import PhotoCreate, Photo, PhotoUpdate
from ...schemas.shared import HTTPError
from ...schemas.user import User
from ...services import photo_service
from ...services.exceptions import (
    ServiceError,
    NotFound,
    NotResourceOwner,
    AlreadyExists,
)


@router.get("/", name="Get photos metadata")
def get_list_metadata(db: Annotated[Session, Depends(get_db)]) -> List[Photo]:
    return photo_service.get_all_photos_metadata(db)


@router.post(
    "/",
    name="Upload photo",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPError},
    },
)
def create(
    file: Annotated[UploadFile, File()],
    description: Annotated[str, Form()],
    db: Annotated[Session, Depends(get_db)],
    file_repository: Annotated[FileRepository, Depends(get_file_repository)],
    user: Annotated[User, Depends(get_current_user)],
) -> Photo:
    photo_create = PhotoCreate(description=description)

    try:
        photo = photo_service.create_photo(
            db, file_repository, photo_create, user, file
        )
    except ServiceError:
        raise HTTPException(status_code=503, detail="Service Unavailable")
    return photo


@router.get(
    "/{id:int}",
    name="Get photo metadata",
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPError}},
)
def get_metadata(id: int, db: Annotated[Session, Depends(get_db)]) -> Photo:
    try:
        return photo_service.get_photo_metadata(db, id)
    except NotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo Not Found"
        )


@router.get(
    "/{id:int}/file",
    name="Get photo file",
    response_class=FileResponse,
    responses={status.HTTP_404_NOT_FOUND: {"model": HTTPError}},
)
def get_data(
    id: int,
    db: Annotated[Session, Depends(get_db)],
    file_repository: Annotated[FileRepository, Depends(get_file_repository)],
):
    try:
        return FileResponse(photo_service.get_photo_filepath(db, file_repository, id))
    except NotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo Not Found"
        )
    except ServiceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The storage service encountered an error.",
        )


@router.put(
    "/{id:int}",
    name="Update photo metadata",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPError},
        status.HTTP_403_FORBIDDEN: {"model": HTTPError},
        status.HTTP_404_NOT_FOUND: {"model": HTTPError},
    },
)
def update(
    new_photo: PhotoUpdate,
    id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
) -> Photo:
    try:
        return photo_service.update_photo_metadata(db, id, new_photo, user)
    except NotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo Not Found"
        )
    except NotResourceOwner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized"
        )


@router.put(
    "/{id:int}/file",
    name="Update photo file",
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPError},
        status.HTTP_403_FORBIDDEN: {"model": HTTPError},
        status.HTTP_404_NOT_FOUND: {"model": HTTPError},
    },
)
def update_data(
    file: Annotated[UploadFile, File()],
    id: int,
    db: Annotated[Session, Depends(get_db)],
    file_repository: Annotated[FileRepository, Depends(get_file_repository)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        return photo_service.update_photo_file(db, file_repository, id, user, file)
    except NotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo Not Found"
        )
    except NotResourceOwner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized"
        )
    except ServiceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The storage service encountered an error.",
        )


@router.delete(
    "/{id:int}",
    name="Delete photo",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPError},
        status.HTTP_403_FORBIDDEN: {"model": HTTPError},
        status.HTTP_404_NOT_FOUND: {"model": HTTPError},
    },
)
def delete(
    id: int,
    db: Annotated[Session, Depends(get_db)],
    file_repository: Annotated[FileRepository, Depends(get_file_repository)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        photo_service.delete_photo(db, file_repository, id, user)
    except NotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Photo Not Found"
        )
    except NotResourceOwner:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not Authorized"
        )
    except ServiceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The storage service encountered an error.",
        )


@router.post(
    "/{id:int}/like",
    name="Like",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPError},
        status.HTTP_404_NOT_FOUND: {"model": HTTPError},
        status.HTTP_409_CONFLICT: {"model": HTTPError},
    },
)
def like(
    id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        photo_service.like(db, id, user)
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except AlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Photo Already Liked"
        )


@router.delete(
    "/{id:int}/like",
    name="Dislike",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": HTTPError},
        status.HTTP_404_NOT_FOUND: {"model": HTTPError},
    },
)
def dislike(
    id: int,
    db: Annotated[Session, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
):
    try:
        photo_service.dislike(db, id, user)
    except NotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

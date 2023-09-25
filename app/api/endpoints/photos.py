from typing import Annotated

from fastapi import Depends, UploadFile, Form, File, HTTPException, status
from sqlalchemy.orm import Session

from ...core.dependencies import get_db, get_file_repository, get_current_user
from ...repositories.file_repository import FileRepository
from ...routers.photos import router
from ...schemas.photo import PhotoCreate
from ...schemas.user import User
from ...services import photo_service
from ...services.exceptions import CreateError


@router.get("/", name="Get photos metadata")
def get_list_metadata(db: Annotated[Session, Depends(get_db)]):
    pass


@router.post("/", name="Upload photo", status_code=status.HTTP_201_CREATED,)
def create(
    file: Annotated[UploadFile, File()],
    description: Annotated[str, Form()],
    db: Annotated[Session, Depends(get_db)],
    file_repository: Annotated[FileRepository, Depends(get_file_repository)],
    user: Annotated[User, Depends(get_current_user)],
):
    photo_create = PhotoCreate(description=description, id_owner=user.id)

    try:
        photo = photo_service.create_photo(db, file_repository, photo_create, file)
    except CreateError:
        raise HTTPException(status_code=503, detail="Service Unavailable")
    return photo


@router.get("/{id:int}", name="Get photo metadata")
def get_metadata(id: int, db: Annotated[Session, Depends(get_db)]):
    pass


@router.get("/{id:int}/file", name="Get photo file")
def get_data(id: int, db: Annotated[Session, Depends(get_db)]):
    pass


@router.put("/{id:int}", name="Update photo metadata")
def update(id: int, db: Annotated[Session, Depends(get_db)]):
    pass


@router.put("/{id:int}/file", name="Update photo file")
def update_data(id: int, db: Annotated[Session, Depends(get_db)]):
    pass


@router.delete("/{id:int}", name="Delete photo")
def delete(id: int, db: Annotated[Session, Depends(get_db)]):
    pass

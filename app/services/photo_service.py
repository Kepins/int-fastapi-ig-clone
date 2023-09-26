from fastapi import UploadFile
from sqlalchemy.orm import Session

from .exceptions import CreateError
from ..db.models import PhotoDB
from ..repositories.exceptions import WriteError
from ..repositories.file_repository import FileRepository
from ..schemas.photo import PhotoCreate, Photo


def get_all_photos_metadata(db: Session):
    pass


def create_photo(
    db: Session, file_repository: FileRepository, photo: PhotoCreate, file: UploadFile
) -> Photo:
    db_photo = PhotoDB(**photo.model_dump())
    db.add(db_photo)
    db.flush()
    db.refresh(db_photo)

    # try to save file
    try:
        file_repository.save_file(db_photo.id, file)
    except WriteError:
        # in case of exception
        db.rollback()
        raise CreateError()

    return Photo.model_validate(db_photo)

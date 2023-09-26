from typing import List

from fastapi import UploadFile
from sqlalchemy.orm import Session

from .exceptions import CreateError, NotFound, NotResourceOwner
from ..db.models import PhotoDB
from ..repositories.exceptions import WriteError
from ..repositories.file_repository import FileRepository
from ..schemas.photo import PhotoCreate, Photo, PhotoUpdate
from ..schemas.user import User


def get_all_photos_metadata(db: Session) -> List[Photo]:
    photos_db = db.query(PhotoDB).all()
    return [Photo.model_validate(photo_db) for photo_db in photos_db]


def create_photo(
    db: Session,
    file_repository: FileRepository,
    photo: PhotoCreate,
    user: User,
    file: UploadFile,
) -> Photo:
    db_photo = PhotoDB(**({"id_owner": user.id} | photo.model_dump()))
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


def get_photo_metadata(db: Session, id: int) -> Photo:
    db_photo = db.get(PhotoDB, id)
    if not db_photo:
        raise NotFound()
    return Photo.model_validate(db_photo)


def get_photo_metadata_if_owner(db: Session, id: int, claimed_owner: User) -> Photo:
    db_photo = db.get(PhotoDB, id)
    if not db_photo:
        raise NotFound()
    if db_photo.id_owner != claimed_owner.id:
        raise NotResourceOwner()
    return Photo.model_validate(db_photo)


def update_photo_metadata(
    db: Session, id: int, new_photo: PhotoUpdate, claimed_owner: User
):
    db_photo = db.get(PhotoDB, id)
    if not db_photo:
        raise NotFound()
    if db_photo.id_owner != claimed_owner.id:
        raise NotResourceOwner()

    for field in new_photo.model_dump():
        setattr(db_photo, field, getattr(new_photo, field))
    db.add(db_photo)
    db.flush()
    db.refresh(db_photo)

    return Photo.model_validate(db_photo)

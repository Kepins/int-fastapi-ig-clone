import os
from typing import List

from fastapi import UploadFile
from sqlalchemy import select, and_
from sqlalchemy.orm import Session

from .exceptions import ServiceError, NotFound, NotResourceOwner, AlreadyExists
from ..db.models import PhotoDB, UserDB
from ..db.models.like import likes_association
from ..repositories.exceptions import WriteError, DeleteError, ReadError
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
        raise ServiceError()

    return Photo.model_validate(db_photo)


def get_photo_metadata(db: Session, id: int) -> Photo:
    db_photo = db.get(PhotoDB, id)
    if not db_photo:
        raise NotFound()
    return Photo.model_validate(db_photo)


def get_photo_filepath(
    db: Session, file_repository: FileRepository, id: int
) -> os.PathLike | str:
    db_photo = db.get(PhotoDB, id)
    if not db_photo:
        raise NotFound()
    try:
        return file_repository.get_file_path(id)
    except ReadError:
        raise ServiceError()


def get_photo_metadata_if_owner(db: Session, id: int, claimed_owner: User) -> Photo:
    db_photo = db.get(PhotoDB, id)
    if not db_photo:
        raise NotFound()
    if db_photo.id_owner != claimed_owner.id:
        raise NotResourceOwner()
    return Photo.model_validate(db_photo)


def update_photo_metadata(
    db: Session, id: int, new_photo: PhotoUpdate, claimed_owner: User
) -> Photo:
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


def update_photo_file(
    db: Session,
    file_repository: FileRepository,
    id: int,
    claimed_owner: User,
    file: UploadFile,
) -> Photo:
    db_photo = db.get(PhotoDB, id)
    if not db_photo:
        raise NotFound()
    if db_photo.id_owner != claimed_owner.id:
        raise NotResourceOwner()
    try:
        file_repository.update_file(id, file)
    except DeleteError:
        raise ServiceError()
    except WriteError:
        # This should never happen but if it does the file is deleted and no new file is created
        raise ServiceError()

    return Photo.model_validate(db_photo)


def delete_photo(
    db: Session, file_repository: FileRepository, id: int, claimed_owner: User
) -> None:
    db_photo = db.get(PhotoDB, id)
    if not db_photo:
        raise NotFound()
    if db_photo.id_owner != claimed_owner.id:
        raise NotResourceOwner()

    try:
        file_repository.delete_file(id)
    except DeleteError:
        raise ServiceError()
    db.delete(db_photo)


def like(db: Session, id, user: User):
    db_photo = db.get(PhotoDB, id)
    if not db_photo:
        raise NotFound("Photo Not Found")

    db_user = db.get(UserDB, user.id)
    if db_photo in db_user.liked_photos:
        raise AlreadyExists()
    db_user.liked_photos.append(db_photo)


def dislike(db: Session, id, user: User):
    db_photo = db.get(PhotoDB, id)
    if not db_photo:
        raise NotFound("Photo Not Found")

    db_user = db.get(UserDB, user.id)
    if db_photo not in db_user.liked_photos:
        raise NotFound("Photo Not Liked")
    db_user.liked_photos.remove(db_photo)

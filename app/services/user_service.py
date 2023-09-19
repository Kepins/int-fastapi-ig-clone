from datetime import datetime
from typing import List

from sqlalchemy import or_, and_, not_
from sqlalchemy.orm import Session

from .exceptions import AlreadyExists, NotFound, PasswordNotMatching
from ..db.models import UserDB
from ..schemas.user import User, UserCreate, UserResetPassword
from ..core.security import Hasher


def __get_not_deleted_db_user(db: Session, id: int) -> UserDB | None:
    return (
        db.query(UserDB).where(and_(UserDB.id == id, not_(UserDB.is_deleted))).first()
    )


def get_all_users(db: Session) -> List[User]:
    users_db = db.query(UserDB).where(not_(UserDB.is_deleted)).all()
    return [User.model_validate(user_db) for user_db in users_db]


def create_user(db: Session, user: UserCreate) -> User:
    if (
        db.query(UserDB)
        .filter(or_(UserDB.email == user.email, UserDB.nickname == user.nickname))
        .first()
    ):
        raise AlreadyExists()

    pass_hash = Hasher.get_password_hash(user.password.get_secret_value())
    db_user = UserDB(**user.model_dump(exclude={"password"}), pass_hash=pass_hash)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User.model_validate(db_user)


def get_user_by_id(db: Session, id: int) -> User:
    db_user = __get_not_deleted_db_user(db, id)
    if not db_user:
        raise NotFound()
    return User.model_validate(db_user)


def update_user(db: Session, user: User) -> User:
    db_user = __get_not_deleted_db_user(db, user.id)
    if not db_user:
        raise NotFound()
    for field in user.model_dump():
        setattr(db_user, field, getattr(user, field))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return User.model_validate(db_user)


def reset_password(db: Session, user: User, passwords: UserResetPassword) -> None:
    db_user = __get_not_deleted_db_user(db, user.id)
    if not db_user:
        raise NotFound()
    if not Hasher.verify_password(
        passwords.old_password.get_secret_value(), db_user.pass_hash
    ):
        raise PasswordNotMatching()
    db_user.pass_hash = Hasher.get_password_hash(
        passwords.new_password.get_secret_value()
    )
    db.add(db_user)
    db.commit()


def delete_user_by_id(db: Session, id: int) -> None:
    db_user = __get_not_deleted_db_user(db, id)
    if not db_user:
        raise NotFound()
    db_user.is_deleted = True
    db_user.deletion_date = datetime.utcnow()
    db.add(db_user)
    db.commit()

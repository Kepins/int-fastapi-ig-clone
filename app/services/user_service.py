from typing import List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from .exceptions import AlreadyExists, NotFound
from ..db.models import UserDB
from ..schemas.user import User, UserCreate
from ..core.security import Hasher


def get_all_users(db: Session) -> List[User]:
    users_db = db.query(UserDB).all()
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
    if db_user := db.get(UserDB, id):
        return User.model_validate(db_user)
    raise NotFound()

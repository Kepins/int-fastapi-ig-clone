from factory import Sequence, SubFactory
from factory.alchemy import SQLAlchemyModelFactory

from app.core.security import Hasher
from app.db.models import UserDB, PhotoDB
from tests.conftest import db


class UserDBFactory(SQLAlchemyModelFactory):
    class Meta:
        model = UserDB
        sqlalchemy_session = db
        sqlalchemy_session_persistence = "flush"
        sqlalchemy_get_or_create = (
            "nickname",
            "email",
        )

    nickname = Sequence(lambda n: f"user {n}")
    first_name = Sequence(lambda n: f"Name {n}")
    last_name = Sequence(lambda n: f"Last Name {n}")
    email = Sequence(lambda n: f"email{n}@example.com")
    pass_hash = Hasher.get_password_hash("password")


class PhotoDBFactory(SQLAlchemyModelFactory):
    class Meta:
        model = PhotoDB
        sqlalchemy_session = db
        sqlalchemy_session_persistence = "flush"

    description = "Description"
    owner = SubFactory(UserDBFactory)

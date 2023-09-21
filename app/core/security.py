from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends
from jose import jwt
from passlib.context import CryptContext

from ..core.dependencies import get_settings
from ..core.settings import Settings
from ..schemas.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)


def create_access_token(user: User, settings: Annotated[Settings, Depends(get_settings)]):
    exp = datetime.utcnow() + timedelta(seconds=settings.JWT_EXPIRATION_SECONDS)

    to_encode = {
        "exp": exp,  # expiration datetime
        "iat": datetime.utcnow(),  # issued at
        "user_id": user.id,  # user
    }

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

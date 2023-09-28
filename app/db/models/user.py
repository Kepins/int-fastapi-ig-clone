import datetime
from typing import Optional, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .like import likes_association
from .photo import PhotoDB


class UserDB(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(100), unique=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(320), unique=True)
    pass_hash: Mapped[str] = mapped_column(String(200))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deletion_date: Mapped[Optional[datetime.datetime]] = mapped_column(default=None)

    photos: Mapped[List["PhotoDB"]] = relationship(
        back_populates="owner", primaryjoin=lambda: UserDB.id == PhotoDB.id_owner
    )

    liked_photos = relationship(
        "PhotoDB", secondary=likes_association, back_populates="likers"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id!r})"

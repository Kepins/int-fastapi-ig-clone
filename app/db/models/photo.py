from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class PhotoDB(Base):
    __tablename__ = "photo"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(500))

    id_owner: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["UserDB"] = relationship(
        back_populates="photos", foreign_keys=[id_owner]
    )

    def __repr__(self) -> str:
        return f"Photo(id={self.id!r})"

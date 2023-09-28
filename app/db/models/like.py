from sqlalchemy import Table, Column, ForeignKey

from app.db.models.base import Base

likes_association = Table(
    "likes",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("photo_id", ForeignKey("photo.id"), primary_key=True),
)

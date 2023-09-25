from pydantic import BaseModel, Extra, ConfigDict


class PhotoBase(BaseModel, extra=Extra.forbid):
    id_owner: int
    description: str


class PhotoCreate(PhotoBase):
    pass


class Photo(PhotoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

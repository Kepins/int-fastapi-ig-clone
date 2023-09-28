from pydantic import BaseModel, Extra, ConfigDict


class PhotoBase(BaseModel, extra=Extra.forbid):
    description: str


class PhotoCreate(PhotoBase):
    pass


class PhotoUpdate(PhotoBase):
    pass


class Photo(PhotoBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    id_owner: int

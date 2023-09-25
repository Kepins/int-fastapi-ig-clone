from pydantic import BaseModel, ConfigDict


class Status(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"status": "ok"}})
    status: str

from pydantic import BaseModel, ConfigDict


class HTTPError(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"detail": "HTTPException raised."}}
    )
    detail: str

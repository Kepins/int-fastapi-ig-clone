from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from ...core.dependencies import get_db
from ...routers.photos import router


@router.get("/", name="Get photos metadata")
def get_list_metadata(db: Annotated[Session, Depends(get_db)]):
    pass


@router.post("/", name="Upload photo")
def create(db: Annotated[Session, Depends(get_db)]):
    pass


@router.get("/{id:int}", name="Get photo metadata")
def get_metadata(id: int, db: Annotated[Session, Depends(get_db)]):
    pass


@router.get("/{id:int}/file", name="Get photo file")
def get_data(id: int, db: Annotated[Session, Depends(get_db)]):
    pass


@router.put("/{id:int}", name="Update photo metadata")
def update(id: int, db: Annotated[Session, Depends(get_db)]):
    pass


@router.put("/{id:int}/file", name="Update photo file")
def update_data(id: int, db: Annotated[Session, Depends(get_db)]):
    pass


@router.delete("/{id:int}", name="Delete photo")
def delete(id: int, db: Annotated[Session, Depends(get_db)]):
    pass

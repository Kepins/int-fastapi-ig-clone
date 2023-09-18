from fastapi import APIRouter

router = APIRouter(
    prefix="/status",
    tags=["status"],
)

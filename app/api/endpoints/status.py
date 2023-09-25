from ...routers.status import router
from ...schemas.status import Status


@router.get("", name="status")
async def index() -> Status:
    return Status(status="ok")

from ...routers.status import router


@router.get("/")
async def index():
    return {"status": "ok"}

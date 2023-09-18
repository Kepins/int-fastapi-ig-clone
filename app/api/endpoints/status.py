from ...routers.status import router


@router.get("/", name="status")
async def index():
    return {"status": "ok"}

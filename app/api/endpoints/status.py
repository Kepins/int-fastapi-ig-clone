from ...routers.status import router


@router.get("/")
async def root():
    return {"status": "ok"}

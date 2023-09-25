from fastapi import FastAPI

from .routers import status, users, account, photos

app = FastAPI()

app.include_router(status.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(account.router, prefix="/api")
app.include_router(photos.router, prefix="/api")

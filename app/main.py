from fastapi import FastAPI

from .routers import status, users


app = FastAPI()

app.include_router(status.router, prefix="/api")
app.include_router(users.router, prefix="/api")

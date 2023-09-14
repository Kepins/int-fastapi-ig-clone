from fastapi import FastAPI

from .routers import status


app = FastAPI()

app.include_router(status.router)

from fastapi import FastAPI

from app.config.settings import settings
from app.routers import root, health_check

app = FastAPI(
    title=settings.fastapi.title,
    version=settings.fastapi.version,
    description=settings.fastapi.description,
)

app.include_router(root.router)
app.include_router(health_check.router)

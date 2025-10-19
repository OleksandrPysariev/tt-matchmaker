import logging

from fastapi import FastAPI

from app.config.settings import settings
from app.routers import root, health_check, matchmaking

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(name)s - %(message)s",
)

app = FastAPI(
    title=settings.fastapi.title,
    version=settings.fastapi.version,
    description=settings.fastapi.description,
)

app.include_router(root.router)
app.include_router(health_check.router)
app.include_router(matchmaking.router)

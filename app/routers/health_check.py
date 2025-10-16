from fastapi import APIRouter

from app.config.settings import settings
from app.models.healthcheck import HealthState

router = APIRouter(tags=["health_check"])


@router.get("/healthcheck", include_in_schema=False)
async def check_health() -> HealthState:
    return HealthState(
        service_name=settings.fastapi.title,
        environment=settings.fastapi.environment,
        version=settings.fastapi.version,
        status="alive",
    )

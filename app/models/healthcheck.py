from pydantic import BaseModel

from app.enums.common import EnvironmentEnum


class HealthState(BaseModel):
    service_name: str
    environment: EnvironmentEnum
    version: str
    status: str

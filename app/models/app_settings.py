from pydantic_settings import BaseSettings, SettingsConfigDict


class AppBaseSettings(BaseSettings):
    """Base class to inherit for settings"""

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


class FastAPISettings(AppBaseSettings):
    environment: str = "LOCAL"
    debug: bool = True
    title: str = "Billing Registry Service"
    description: str = "Billing Registry Service API"
    version: str = "0.0.1"

    model_config = SettingsConfigDict(env_prefix="fastapi")


class MatchmakingSettings(AppBaseSettings):
    max_team_size: int = 6


class Settings(BaseSettings):
    fastapi: FastAPISettings = FastAPISettings()
    matchmaking: MatchmakingSettings = MatchmakingSettings()

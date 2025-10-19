from pydantic import BaseModel

from app.models.common.match import Match


class SimpleMatchmakingOutput(BaseModel):
    matches: list[Match] | None


class SquadMatchmakingOutput(SimpleMatchmakingOutput):
    pass


class WaitlistSquadMatchmakingOutput(SquadMatchmakingOutput):
    pass

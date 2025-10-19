from pydantic import BaseModel

from app.models.common.match import Match, WaitlistSquadMatch, SquadMatch


class SimpleMatchmakingOutput(BaseModel):
    matches: list[Match] | None


class SquadMatchmakingOutput(SimpleMatchmakingOutput):
    matches: list[SquadMatch] | None


class WaitlistSquadMatchmakingOutput(SquadMatchmakingOutput):
    matches: list[WaitlistSquadMatch] | None

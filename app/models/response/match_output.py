from typing import Annotated

from pydantic import BaseModel, Field

from app.models.common.match import Match
from app.models.response.player_output import (
    PlayerOutput,
    SquadPlayerOutput,
    WaitlistSquadPlayerOutput,
)


class MatchOutput(Match):
    teams: Annotated[list[list[PlayerOutput]], Field(min_length=2, max_length=2)]


class SquadMatchOutput(MatchOutput):
    teams: Annotated[list[list[SquadPlayerOutput]], Field(min_length=2, max_length=2)]


class WaitlistSquadMatchOutput(SquadMatchOutput):
    teams: Annotated[list[list[WaitlistSquadPlayerOutput]], Field(min_length=2, max_length=2)]

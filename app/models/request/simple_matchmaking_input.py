from typing import Annotated

from pydantic import Field

from app.models.common.player import Player, SquadPlayer, WaitlistSquadPlayer
from app.models.common.simple_matchmaking import SimpleMatchmaking, SquadMatchmaking, WaitlistSquadMatchmaking


class SimpleMatchmakingInput(SimpleMatchmaking):
    players: Annotated[list[Player], Field(max_length=2000, min_length=1000)]


class SquadMatchmakingInput(SquadMatchmaking):
    players: Annotated[list[SquadPlayer], Field(max_length=2000, min_length=1000)]


class WaitlistSquadMatchmakingInput(WaitlistSquadMatchmaking):
    players: Annotated[list[WaitlistSquadPlayer], Field(max_length=2000, min_length=1000)]

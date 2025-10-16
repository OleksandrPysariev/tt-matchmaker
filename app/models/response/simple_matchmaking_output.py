from pydantic import BaseModel

from app.models.common.simple_matchmaking import SimpleMatchmaking, SquadMatchmaking, WaitlistSquadMatchmaking
from app.models.response.player_output import PlayerOutput, SquadPlayerOutput, WaitlistSquadPlayerOutput


# class SimpleMatchmakingOutput(SimpleMatchmaking):
#     players: list[PlayerOutput]

class SimpleMatchmakingOutput(BaseModel):
    match: list[list[PlayerOutput]]


class SquadMatchmakingOutput(SquadMatchmaking):
    players: list[SquadPlayerOutput]


class WaitlistSquadMatchmakingOutput(WaitlistSquadMatchmaking):
    players: list[WaitlistSquadPlayerOutput]

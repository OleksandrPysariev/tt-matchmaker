from pydantic import BaseModel

from app.models.common.player import Player, SquadPlayer, WaitlistSquadPlayer


# Simple Matchmaking scheme.


class SimpleMatchmaking(BaseModel):
    players: list[Player]


class SquadMatchmaking(SimpleMatchmaking):
    players: list[SquadPlayer]


class WaitlistSquadMatchmaking(SquadMatchmaking):
    players: list[WaitlistSquadPlayer]

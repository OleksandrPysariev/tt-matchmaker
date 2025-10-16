from app.models.common.player import Player
from app.models.common.simple_matchmaking import SimpleMatchmaking, SquadMatchmaking, WaitlistSquadMatchmaking
from app.models.request.player_input import PlayerInput, SquadPlayerInput, WaitlistSquadPlayerInput


class SimpleMatchmakingInput(SimpleMatchmaking):
    players: list[Player]


class SquadMatchmakingInput(SquadMatchmaking):
    players: list[SquadPlayerInput]


class WaitlistSquadMatchmakingInput(WaitlistSquadMatchmaking):
    players: list[WaitlistSquadPlayerInput]

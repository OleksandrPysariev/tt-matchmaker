from app.models.common.match import Match
from app.models.common.player import Player
from app.services.matchmaking.base import BaseMatchmakingService


class SimpleMatchmakingService(BaseMatchmakingService):
    def do_matchmaking(self, players: list[Player]) -> Match:
        return


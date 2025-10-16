from abc import ABC, abstractmethod

from app.models.common.match import Match
from app.models.common.player import Player


class BaseMatchmakingService(ABC):
    @abstractmethod
    def do_matchmaking(self, players: list[Player]) -> Match:
        pass

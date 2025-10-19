from copy import copy
from typing import TypeVar, Generic, Type

from app.models.common.player import Player, SquadPlayer, WaitlistSquadPlayer

PlayerType = TypeVar("PlayerType", bound=Player)


class BasePlayersDB(Generic[PlayerType]):
    def __init__(self, player_class: Type[PlayerType]) -> None:
        self.player_class = player_class
        self._storage: list[PlayerType] = []

    def store_new_players(self, players: list[PlayerType]) -> None:
        if len(players) == 0:
            return

        if not all(isinstance(player, self.player_class) for player in players):
            raise TypeError(f"All players must be instances of {self.player_class.__name__}")

        # Get existing player IDs
        existing_ids = {player.id for player in self._storage}

        # Filter out players that are already in the database
        new_players = [player for player in players if player.id not in existing_ids]

        if len(new_players) == 0:
            return

        copy_storage = copy(self._storage)
        copy_storage.extend(new_players)
        self._storage = copy_storage

    def get_all_players(self) -> list[PlayerType]:
        return copy(self._storage)

    def clear(self) -> None:
        self._storage = []


players_db = BasePlayersDB[Player](Player)
squad_players_db = BasePlayersDB[SquadPlayer](SquadPlayer)
waitlist_squad_players_db = BasePlayersDB[WaitlistSquadPlayer](WaitlistSquadPlayer)

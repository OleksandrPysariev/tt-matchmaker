from typing import Annotated

from pydantic import BaseModel, Field

from app.config.settings import settings
from app.models.common.player import Player, SquadPlayer, WaitlistSquadPlayer


class Team(BaseModel):
    players: Annotated[
        list[Player],
        Field(
            description="A list of 6 players.",
            max_length=settings.matchmaking.max_team_size,
        ),
    ] = list()

    def calc_disbalance(self) -> float:
        players_skill_list = [player.skill for player in self.players]
        mean_skill = sum(players_skill_list) / len(players_skill_list)
        return round(
            sum(abs(player_skill - mean_skill) for player_skill in players_skill_list) / len(players_skill_list), 1
        )


class SquadTeam(Team):
    players: Annotated[
        list[SquadPlayer],
        Field(
            description="A list of 6 players.",
            max_length=settings.matchmaking.max_team_size,
        ),
    ] = list()


class WaitlistSquadTeam(SquadTeam):
    players: Annotated[
        list[WaitlistSquadPlayer],
        Field(
            description="A list of 6 players.",
            max_length=settings.matchmaking.max_team_size,
        ),
    ] = list()

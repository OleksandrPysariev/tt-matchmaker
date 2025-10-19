from typing import Annotated

from pydantic import BaseModel, Field

from app.models.common.team import Team, SquadTeam, WaitlistSquadTeam


class Match(BaseModel):
    teams: Annotated[list[Team], Field(min_length=2, max_length=2)]

    def calc_disbalance(self) -> int:
        team1_skill_sum = sum([player.skill for player in self.teams[0].players])
        team2_skill_sum = sum([player.skill for player in self.teams[1].players])
        return abs(team1_skill_sum - team2_skill_sum)


class SquadMatch(Match):
    teams: Annotated[list[SquadTeam], Field(min_length=2, max_length=2)]


class WaitlistSquadMatch(SquadMatch):
    teams: Annotated[list[WaitlistSquadTeam], Field(min_length=2, max_length=2)]

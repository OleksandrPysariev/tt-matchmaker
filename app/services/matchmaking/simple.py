from app.config.settings import settings
from app.models.common.match import Match
from app.models.common.player import Player
from app.models.common.team import Team
from app.services.matchmaking.base import BaseMatchmakingService
from app.storage.players_db import BasePlayersDB


class SimpleMatchmakingService(BaseMatchmakingService):
    def __init__(self, players_db: BasePlayersDB, max_players: int = None) -> None:
        self.players_db = players_db
        self.MAX_PLAYERS = max_players or settings.matchmaking.max_team_size

    def do_matchmaking(self, new_players: list[Player]) -> list[Match] | None:
        # Usually, I would do atomic updates (get by id, put into the team, remove from db),
        # but let's pretend this is okay for the sake of me finishing this faster.

        # This solution doesn't handle skill outliers well. Important to put high-skilled outliers
        # through a longer waiting queue in favor of match balance, but that requires waiting time aware matchmaking.

        # 1. get all existing players from DB
        existing_players = self.players_db.get_all_players()
        # 3. combine old and new
        all_players = existing_players + new_players
        # 4. sort players to improve skill balance during greedy matching
        sorted_players = list(sorted(all_players, key=lambda player: player.skill, reverse=True))

        resulting_matches = []
        team1, team2 = Team(), Team()
        skill_sum1, skill_sum2 = 0, 0

        while len(sorted_players) >= self.MAX_PLAYERS:
            # The strategy is to pop a player from the top of the list and put them in a team.
            # To make the match balanced (a balanced match is a match among similar skilled players), the script
            # checks the total skill level of the team and assigns the next player to the weaker team.
            player = sorted_players[0]
            if len(team1.players) < self.MAX_PLAYERS and (
                skill_sum1 <= skill_sum2 or len(team2.players) == self.MAX_PLAYERS
            ):
                team1.players.append(player)
                skill_sum1 += player.skill
                sorted_players.pop(0)
            elif len(team2.players) < self.MAX_PLAYERS:
                team2.players.append(player)
                skill_sum2 += player.skill
                sorted_players.pop(0)
            else:
                match = Match(teams=[team1, team2])
                resulting_matches.append(match)
                team1, team2 = Team(players=[player]), Team()
                skill_sum1, skill_sum2 = player.skill, 0
                sorted_players.pop(0)

        # 5. store leftover players back into DB for later matching
        self.players_db.store_new_players(sorted_players)
        return resulting_matches

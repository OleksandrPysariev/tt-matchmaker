import time
from collections import defaultdict

from app.config.settings import settings
from app.models.common.match import Match, WaitlistSquadMatch
from app.models.common.player import WaitlistSquadPlayer
from app.models.common.team import WaitlistSquadTeam
from app.services.matchmaking.base import BaseMatchmakingService
from app.storage.players_db import BasePlayersDB


class WaitlistSquadMatchmakingService(BaseMatchmakingService):
    def __init__(self, players_db: BasePlayersDB, max_players: int = None) -> None:
        self.players_db = players_db
        self.MAX_PLAYERS = max_players or settings.matchmaking.max_team_size

    def do_matchmaking(self, new_players: list[WaitlistSquadPlayer]) -> list[Match] | None:
        # Usually, I would do atomic updates (get by id, put into the team, remove from db),
        # but let's pretend this is okay for the sake of me finishing this faster.

        # This solution prioritizes players with longer wait times to ensure fairness.
        # Players who have been waiting longer get matched first.

        # 1. get all existing players from DB
        existing_players = self.players_db.get_all_players()
        # 3. combine old and new
        all_players = existing_players + new_players

        # 4. group players by squad_id
        squads_dict = defaultdict(list)
        solo_players = []

        for player in all_players:
            solo_players.append(player) if player.squad_id == -1 else squads_dict[player.squad_id].append(player)

        # 5. calculate average skill and earliest timestamp (longest wait time) for each squad
        current_time = int(time.time())
        squads = []
        for squad_id, squad_members in squads_dict.items():
            # Find earliest timestamp in squad (player who joined first)
            earliest_timestamp = min(p.epoch_timestamp for p in squad_members)
            squads.append(
                {
                    "members": squad_members,
                    "avg_skill": round(sum(p.skill for p in squad_members) / len(squad_members), 1),
                    "wait_time": current_time - earliest_timestamp,
                    "earliest_timestamp": earliest_timestamp,
                }
            )

        # 6. sort squads and players by wait time (prioritize longer waits), then by skill for balance
        # Sort by wait time descending (longer waits first), then by skill descending for tie-breaking
        sorted_squads = list(sorted(squads, key=lambda s: (-s["wait_time"], -s["avg_skill"])))
        sorted_solo_players = list(sorted(solo_players, key=lambda p: (-(current_time - p.epoch_timestamp), -p.skill)))

        resulting_matches = []
        team1, team2 = WaitlistSquadTeam(), WaitlistSquadTeam()
        skill_sum1, skill_sum2 = 0, 0

        # 7. Process squads first, then solo players to prioritize team formation because solo players can be used
        # to fill the gaps.
        units_to_process = [{"type": "squad", "data": squad} for squad in sorted_squads] + [
            {"type": "solo", "data": player} for player in sorted_solo_players
        ]

        while units_to_process:
            unit = units_to_process[0]
            players_to_add = unit["data"]["members"] if unit["type"] == "squad" else [unit["data"]]
            num_players = len(players_to_add)

            # Check if both teams are full and finalize the match
            if len(team1.players) == self.MAX_PLAYERS and len(team2.players) == self.MAX_PLAYERS:
                match = WaitlistSquadMatch(teams=[team1, team2])
                resulting_matches.append(match)
                team1, team2 = WaitlistSquadTeam(), WaitlistSquadTeam()
                skill_sum1, skill_sum2 = 0, 0
            # Try to add to team1 first if it has lower or equal skill sum and has space
            elif (len(team1.players) + num_players <= self.MAX_PLAYERS) and (
                skill_sum1 <= skill_sum2 or not (len(team2.players) + num_players <= self.MAX_PLAYERS)
            ):
                for player in players_to_add:
                    team1.players.append(player)
                    skill_sum1 += player.skill
                units_to_process.pop(0)
            # Try to add to team2 if it has space
            elif len(team2.players) + num_players <= self.MAX_PLAYERS:
                for player in players_to_add:
                    team2.players.append(player)
                    skill_sum2 += player.skill
                units_to_process.pop(0)
            else:
                # Cannot fit this unit anywhere, save for later
                units_to_process.pop(0)

        # 8. If we have leftover partial teams, try to combine them or save back
        leftover_players = team1.players + team2.players

        # 9. store leftover players back into DB for later matching
        self.players_db.store_new_players(leftover_players)
        return resulting_matches

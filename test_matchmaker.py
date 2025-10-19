import json

from app.models.request.simple_matchmaking_input import SimpleMatchmakingInput
from app.services.matchmaking.simple import SimpleMatchmakingService
from app.storage.players_db import players_db

if __name__ == '__main__':
    with open('simple_players_input.json', 'r') as f:
        players = dict()
        players["players"] = json.load(f)
        matchmaking_input = SimpleMatchmakingInput.model_validate(players)
        matches = SimpleMatchmakingService(players_db=players_db).do_matchmaking(matchmaking_input.players)
        print(matches)

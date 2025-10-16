from app.models.common.player import Player, SquadPlayer, WaitlistSquadPlayer


# Models for Player scheme request parsing. Adjust if necessary.


class PlayerInput(Player):
    pass


class SquadPlayerInput(SquadPlayer):
    pass


class WaitlistSquadPlayerInput(WaitlistSquadPlayer):
    pass

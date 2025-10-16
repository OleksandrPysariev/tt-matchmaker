from app.models.common.player import Player, SquadPlayer, WaitlistSquadPlayer


# Models for Player scheme request parsing. Adjust if necessary.


class PlayerOutput(Player):
    pass


class SquadPlayerOutput(SquadPlayer):
    pass


class WaitlistSquadPlayerOutput(WaitlistSquadPlayer):
    pass

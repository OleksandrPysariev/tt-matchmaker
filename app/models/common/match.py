from pydantic import BaseModel

from app.models.common.player import Player


class Match(BaseModel):
    players: list[list[Player]]

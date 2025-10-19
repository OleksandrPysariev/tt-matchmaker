from pydantic import BaseModel, Field


class Player(BaseModel):
    id: str = Field(
        alias="ID",
        description="Unique identifier of player in hexadecimal format.",
        examples=["0x123A89", "0x4E3A12"]
    )
    skill: int = Field(
        alias="Skill",
        description="Positive integer value of the player's rank.",
        examples=[12, 812, 264]
    )

    def __repr__(self):
        return f"{self.id}: skill {self.skill}"


class SquadPlayer(Player):
    squad_id: int = Field(
        alias="SquadId",
        description="Integer ID of squad the player belongs to. No squad is -1",
        examples=[-1, 157, 22]
    )

    def __repr__(self):
        return f"{self.id}: skill {self.skill}, squad {self.squad_id}"


class WaitlistSquadPlayer(SquadPlayer):
    wait_time_sec: int = Field(
        alias="WaitTimeSec",
        description="Wait time of player in queue in seconds.",
        examples=[0, 5, 360]
    )

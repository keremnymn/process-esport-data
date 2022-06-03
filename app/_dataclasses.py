from dataclasses import dataclass, field
from typing import Dict, List
from datetime import datetime
from enum import Enum


class TurretLane(Enum):
    bot = 0
    mid = 1
    top = 3


class DragonType(Enum):
    water = 0
    air = 1
    earth = 2


@dataclass
class Player:
    """
    there are totalGold and currentGold variables in Player but nothing actually
    substracts from either of these fields, so I'm just counting 'gold' variable.
    """

    gold: int = 500
    alive: bool = True
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    minions: int = 0
    name: str = ""


@dataclass
class Turret:
    turretTier: int = 1
    turretLane: TurretLane = TurretLane.bot

    turrent_mapping = {
        "bot": TurretLane.bot,
        "mid": TurretLane.mid,
        "top": TurretLane.top,
    }

    def __post_init__(self):
        self.turretLane = self.turrent_mapping[self.turretLane]

    def __repr__(self):
        return f"tier {self.turretTier} {self.turretLane.name} turret"


@dataclass
class Dragon:
    dragonType: DragonType = DragonType.water

    dragon_mapping = {
        "water": DragonType.water,
        "air": DragonType.air,
        "earth": DragonType.earth,
    }

    def __post_init__(self):
        self.dragonType = self.dragon_mapping[self.dragonType]

    def __repr__(self):
        return self.dragonType.name


@dataclass
class Team:
    teamID: str = ""
    name: str = ""
    nashorKills: int = 0
    killed_dragons: List[Dragon] = field(default_factory=list)
    destroyed_turrets: List[Turret] = field(default_factory=list)
    players: Dict[str, Player] = field(default_factory=dict)

    def add_player(self, id: str, player: Player) -> None:
        self.players[id] = player

    @property
    def dragonKills(self) -> int:
        return len(self.killed_dragons)

    @property
    def towersDestroyed(self) -> int:
        return len(self.destroyed_turrets)


@dataclass
class Fixture:
    seriesCurrent: int
    seriesType: str
    title: str
    seriesMax: int
    startTime: datetime

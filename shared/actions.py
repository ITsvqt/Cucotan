#shared actions definition

from dataclasses import dataclass
from typing import Literal, Union


@dataclass(frozen=True)
class BuildRoad:
    player_id: int
    edge_id: int


@dataclass(frozen=True)
class BuildSettlement:
    player_id: int
    vertex_id: int


@dataclass(frozen=True)
class RollDice:
    player_id: int


@dataclass(frozen=True)
class EndTurn:
    player_id: int


@dataclass(frozen=True)
class EndTurn:
    player_id: int
    
GameAction = Union[
    BuildRoad,
    BuildSettlement,
    RollDice,
    EndTurn
]

    

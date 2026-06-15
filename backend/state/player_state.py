from dataclasses import dataclass

@dataclass
class PlayerState:
    id: int
    name: str

    resources: dict[str, int]
    victory_points: int = 0
from dataclasses import dataclass
from backend.core.enums import Terrain

@dataclass(slots=True)
class Hex:
    id: int
    terrain = Terrain
    number: int
    vertex_ids: list[int]
    edge_ids: list[int]
    
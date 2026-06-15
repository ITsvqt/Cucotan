from dataclasses import dataclass

@dataclass(slots=True)
class Vertex:
    id: int
    edge_ids: list[int]
    hex_ids: list[int]
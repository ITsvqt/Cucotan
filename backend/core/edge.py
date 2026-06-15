from dataclasses import dataclass

@dataclass(slots=True)
class Edge:
    id: int
    vertex_ids: tuple[int, int]
    hex_ids: list[int]
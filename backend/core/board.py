from dataclasses import dataclass, field
from backend.core.vertex import Vertex
from backend.core.edge import Edge
from backend.core.hex import Hex

@dataclass
class Board:
    vertices: dict[int, Vertex]
    edges: dict[int, Edge]
    hexes: dict[int, Hex]

    def neighbors(self, vertex_id: int) -> list[int]:
        v = self.vertices[vertex_id]
        result = []

        for e_id in v.edge_ids:
            e = self.edges[e_id]
            a, b = e.vertex_ids
            result.append(b if a == vertex_id else a)

        return result
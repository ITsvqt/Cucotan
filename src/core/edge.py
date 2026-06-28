from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.vertex import Vertex
    from core.hex import Hex

class Edge:
    def __init__(self, edge_id: int):
        self._edge_id = edge_id
        # hexagons edge connects
        self._adjacent_hexes: tuple[Hex, ...] = ()         # 1 or 2
        self._adjacent_vertices: tuple[Vertex, Vertex] = () # always 2
        # all possible edges from the 2 vertices it connects( excluding self )
        self._adjacent_edges: tuple[Edge, ...] = ()        # 2, 3 or 4
        
    def wire(self,
        adjacent_hexes:    tuple[Hex, ...],
        adjacent_vertices: tuple[Vertex, Vertex],
        adjacent_edges:    tuple[Edge, ...]) -> None:
        """
            Called once by Board after all vertices and edges are created
        """
    
        self._adjacent_hexes    = adjacent_hexes
        self._adjacent_vertices = adjacent_vertices
        self._adjacent_edges    = adjacent_edges   
        
## PROPERTIES
    @property
    def edge_id(self):
        return self._edge_id
    @property
    def adjacent_vertices(self):
        return self._adjacent_vertices
    @property
    def adjacent_hexes(self):
        return self._adjacent_hexes
    @property
    def adjacent_edges(self):
        return self._adjacent_edges
    
## DUNDER
    def __repr__(self) -> str:
        return f"Edge({self._edge_id})"

    def __hash__(self) -> int:
        return hash(self._edge_id)
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Edge) and self._edge_id == other._edge_id
    
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.vertex import Vertex
    from core.hex import Hex

class Edge:
    
    """ This is the road. """
    
    
    def __init__(self, edge_id: int):
        
        # For serialization in state
        self._edge_id = edge_id
        
        # The 2 hexes the road touches 
        # (it would be 1 or 2 if sea was not an actuall hex)
        # (ONLY USED FOR FINDING THE OUTLINE OF THE BOARD)
        self._adjacent_hexes: tuple[Hex, ...] = ()
        
        # Every edge connects 2 vertex
        self._adjacent_vertices: tuple[Vertex, Vertex] = ()
        
        # Other edges coming after self
        # From 2 to 4
        # All possible edges from the 2 vertices it connects( excluding self )
        self._adjacent_edges: tuple[Edge, ...] = ()
        
    def wire_vertices(self, adjacent_vertices: tuple[Vertex, Vertex]):
        self._adjacent_vertices = adjacent_vertices
        
    def wire_hexes(self, adjacent_hexes: tuple[Hex, ...]):
        self._adjacent_hexes = adjacent_hexes
        
    def wire_edges(self, adjacent_edges: tuple[Edge]):
        self._adjacent_edges = adjacent_edges
        
    def wire(self,
        adjacent_hexes:    tuple[Hex, ...],
        adjacent_vertices: tuple[Vertex, Vertex],
        adjacent_edges:    tuple[Edge, ...]
        ) -> None:
        
        """ Called once by Board after all vertices and edges are created. """
    
        self._adjacent_hexes    = adjacent_hexes
        self._adjacent_vertices = adjacent_vertices
        self._adjacent_edges    = adjacent_edges   
        
    #* PROPERTIES
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
    
    #* DUNDER
    def __repr__(self) -> str:
        return f"Edge({self._edge_id})"

    def __hash__(self) -> int:
        return hash(self._edge_id)
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Edge) and self._edge_id == other._edge_id
    
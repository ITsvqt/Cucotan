
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.enums.resource import Resource
    from core.enums.terrain import Terrain
    from core.vertex import Vertex
    from core.edge import Edge
    

class Hex:
    
    def __init__(self):
        self._hex_id: int = None # for serialization in state/
        self._number: int = None # None for the desert, 2–12 otherwise
        self._resource_type: Terrain = None
        
        self._vertices: list[Vertex] = [] # len == 6
        self._edges:    list[Edge]   = [] # len == 6
    
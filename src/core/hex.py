
from enums import Terrain, PortType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.vertex import Vertex
    from core.edge import Edge
    

class Hex:
    def __init__(self, hex_id:int, terrain: Terrain, number: int | None, port: PortType | None):
        # for serialization in state
        self._hex_id: int = hex_id 
        self._terrain: Terrain = terrain
        self._number: int | None = number           # None for the desert and sea, 2–12 otherwise
        self._port: PortType | None = port  # for sea hex with port
              
        self._vertices: tuple[Vertex, ...] = () # 6 for land, fewer for sea outer ring
        self._edges:    tuple[Edge  , ...] = () # same count as vertices
    
    def wire(self,
        adjacent_vertices: tuple[Vertex, ...],
        adjacent_edges:    tuple[Edge, ...]) -> None:
        """Called once by Board after all vertices and edges are created
        """
        
        self._adjacent_vertices = adjacent_vertices
        self._adjacent_edges    = adjacent_edges    
         
    #* CLASS METHODS
    # factory methods
    @classmethod
    def land(cls, hex_id:int, terrain: Terrain, number: int):
        return cls(hex_id, terrain, number, port = None)

    @classmethod
    def desert(cls, hex_id:int):
        return cls(hex_id, Terrain.DESERT, number = None, port = None)

    @classmethod
    def sea(cls, hex_id:int, port: PortType | None):
        return cls(hex_id, Terrain.SEA, number = None, port = port)

    #* PROPERTIES
    @property
    def hex_id(self):
        return self._hex_id
    @property
    def terrain(self):
        return self._terrain
    @property
    def number(self):
        return self._number
    @property
    def port(self):
        return self._port
    @property
    def vertices(self):
        return self._vertices
    @property
    def edges(self):
        return self._edges
    
    #* DUNDER
    def __repr__(self):
        return f"Hex({self._hex_id}, {self._terrain.value}, {self._number}))"

    def __hash__(self) -> int:
        return hash(self._hex_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Hex) and self._hex_id == other._hex_id

    
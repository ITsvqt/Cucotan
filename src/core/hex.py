
from shared.enums import Terrain, PortType
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.vertex import Vertex
    from core.edge import Edge
    

class Hex:
    
    """ Terrain tile. Produces resource when its number is rolled. """
    
    
    def __init__(
        self,
        hex_id: int, 
        q: int, # left, right
        r: int, # diagonal
        terrain = None
        ):
        
        self._adjacent_vertices: tuple[Vertex, ...] = () # 6 for land, fewer for sea's outer ring
        self._adjacent_edges:    tuple[Edge  , ...] = () # same count as vertices
        
        self._hex_id: int = hex_id 
        self._q = q
        self._r = r
        self._s = -(q + r) #derived

        self._terrain: Terrain = terrain
        self._number: int | None = None   # None for the desert and sea, 2–12 otherwise
        self._port: PortType | None = None  # for sea hex with port
        

        
        
        # deffensive assert to catch wrong __init__ modifications for the cordinates logic
        assert self._q + self._r + self._s == 0, f"Invalid cube coordinates: q={self._q} r={self._r} s={self._s}"
              

    
    def wire(self,
        adjacent_vertices: tuple[Vertex, ...],
        adjacent_edges:    tuple[Edge, ...]
        ) -> None:
        
        """ Called once by Board after all vertices and edges are created. """
        
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
    def q(self):
        return self._q
    @property
    def r(self):
        return self._r    
    @property
    def s(self):
        return self._s
    @property
    def vertices(self):
        return self._adjacent_vertices
    @property
    def edges(self):
        return self._adjacent_edges
    
    #* DUNDER
    def __repr__(self):
        return f"Hex({self._hex_id}, {self._terrain.value}, {self._number}))"

    def __hash__(self) -> int:
        return hash(self._hex_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Hex) and self._hex_id == other._hex_id

    
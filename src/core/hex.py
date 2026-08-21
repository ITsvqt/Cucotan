
from __future__ import annotations
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
        
        self._adjacent_hexes: tuple[Hex, ...] = ()       # 6 for land, fewer for sea hexes
        self._adjacent_vertices: tuple[Vertex, ...] = () # 6 for land, fewer for sea's outer ring
        self._adjacent_edges:    tuple[Edge  , ...] = () # same count as vertices
        
        self._hex_id: int = hex_id 
        self._q = q
        self._r = r
        self._s = -(q + r) #derived

        self._terrain: Terrain = terrain
        self._number: int | None = None   # None for the desert and sea, 2–12 otherwise
        self._port: PortType | None = None  # for sea hex with port
        


    #* PROPERTIES
    @property
    def hex_id(self):
        return self._hex_id
    
    @property
    def terrain(self):
        return self._terrain
    @terrain.setter
    def terrain(self, value:Terrain):
        self._terrain = value
    
    @property
    def number(self):
        return self._number
    
    @property
    def port(self):
        return self._port
    
    @port.setter
    def port(self, value: PortType):
        self._port = value
    
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
    def adjacent_hexes(self):
        return self._adjacent_hexes
    
    @adjacent_hexes.setter
    def adjacent_hexes(self, value: tuple[Hex, ...]):
        self._adjacent_hexes = value
    
    @property
    def adjacent_vertices(self):
        return self._adjacent_vertices
    
    @adjacent_vertices.setter
    def adjacent_vertices(self, value: tuple[Vertex, ...]):
        self._adjacent_vertices = value
    
    @property
    def adjacent_edges(self):
        return self._adjacent_edges
    
    @adjacent_edges.setter
    def adjacent_edges(self, value: tuple[Edge, ...]):
        self._adjacent_edges = value
    
    
    
    #* DUNDER
    def __repr__(self):
        return f"Hex({self._hex_id}, {self._terrain.value}, {self._number}))"

    def __hash__(self) -> int:
        return hash(self._hex_id)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Hex) and self._hex_id == other._hex_id
    
    def __str__(self):
        port_suffix = f" Port: {self._port.name}" if self.port else ""
        return f"[{self._hex_id:<2}]Hex {f"({self.q}, {self.r})":<8} {self.terrain.value}: {self._number}" + port_suffix

    
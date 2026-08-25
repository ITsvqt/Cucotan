from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.hex import Hex
    from core.edge import Edge
    from enums import PortType

class Vertex:

    """ This is where houses and cities are build. """
    
    
    def __init__(self, vertex_id: int):
        
        # For serialization in state
        self._vertex_id = vertex_id
        
        # Corners of every hex the vertex touches
        # Allways 3, but they might me sea if in the corner        
        self._adjacent_hexes: tuple[Hex, ...] = ()
        
        # Every vertex knows which vertices are his neighbours
        # 2 or 3
        self._adjacent_vertices: tuple[Vertex, ...] = ()
        
        # path to neighbors (same count as vertices )
        self._adjacent_edges: tuple[Edge, ...]  = ()
        
        # building on this hex provide port bonus
        self._port: PortType | None = None
        
      
## PROPERTIES
    @property
    def vertex_id(self):
        return self._vertex_id
    
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
    
    @property
    def port(self):
        return self._port
    
    @port.setter
    def port(self, value: PortType):
        self._port = value
    
## DUNDER
    def __repr__(self) -> str:
        return f"Vertex({self._vertex_id})"

    def __hash__(self) -> int:
        return hash(self._vertex_id)
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Vertex) and self._vertex_id == other._vertex_id
    
    def __str__(self):
        port_suffix = f" Port: {self._port.name}" if self.port else ""
        sorted_hex_cords = sorted([(h.q, h.r) for h in self._adjacent_hexes])
        
        coords_str = " ".join(f"({q}, {r})" for q, r in sorted_hex_cords)
        
        return f"[{self._vertex_id:<3}]Vertex {coords_str:<26}" + port_suffix
        
        
        
        
        
#         The distance rule says no two settlements can be on neighboring vertices.
#!        all(v.owner is None for v in vertex.adjacent_vertices)
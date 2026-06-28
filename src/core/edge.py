from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from core.vertex import Vertex

class Edge:
    def __init__(self):
        self._ownder = None
        
    @property
    def owner(self):
        self._verticies: tuple[Vertex, Vertex] = None  # the 2 endpoints
        return self._ownder
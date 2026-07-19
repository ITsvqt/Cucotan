from core.hex import Hex
from core.vertex import Vertex
from core.edge import Edge

# commit msg after completoing board
# Board model(orchestrator) completed

# 95 Resource Cards: 19 each of Brick, Grain, Lumber, Ore, and Wool
# 25 Development Cards: 14 Knights/Soldiers, 6 Progress Cards, and 5 Victory Point Cards.
# Player Pieces (in 4 colors): 16 cities (churches), 20 settlements (houses), and 60 roads (bars).
# Miscellaneous: 2 dice (1 red, 1 yellow), 1 robber, 2 Special Cards ("Longest Road" and "Largest Army"), and 4 "Building Costs" reference cards.


class Board:
    
    """ Responsible for constructing and wiring game objects. """
    
    
    # BALANCED HEX NUMBER DISTRIBUTION
    MAX_DOTS_PER_VERTEX = 13
    
    def __init__(self):
        
        self._hexes:    dict[int, Hex] = {}
        self._vertices: dict[int, Vertex] = {}
        self._edges:    dict[int, Edge] = {}
        self._hex_map:  dict[tuple[int, int], Hex] = {}  # (q, r) Hex for neigbor lookup


        # Board generation
        # self._hexes: list[Hex] = self._create_hexes(land_hexes_cordinates)
    
    # q   r   s( s == -(q+r) )
    DIRECTIONS = [
    (-1, -1,  2),  # top-left
    ( 0, -1,  1),  # top-right
    (-1,  0,  1),  # left
    (+1,  0, -1),  # right
    ( 0, +1, -1),  # bottom-left
    (+1, +1, -2),  # bottom-right
    
    
    
]
    
    
    
    
    
    
    """
Row 1 (top):              (-1,-2)  ( 0,-2)  ( 1,-2)
Row 2:              (-2,-1)  (-1,-1)  ( 0,-1)  ( 1,-1)
Row 3 (mid):  (-2, 0)  (-1, 0)  ( 0, 0)  ( 1, 0)  ( 2, 0)
Row 4:              (-2, 1)  (-1, 1)  ( 0, 1)  ( 1, 1)
Row 5 (bot):              (-1, 2)  ( 0, 2)  ( 1, 2)

Legend:
        q:  - left, +right
        r:  - top_right, + bot_right
        r: with negative q changes to left
        
        s: allways adds up to -(q + r)
    """
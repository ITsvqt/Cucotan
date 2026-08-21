

"""
19 hexes (4 grain; 3ore; 4 wood; 3 clay; 4 sheep) + 1 desert
*
6 vertices each
_______

54 vertices(settlements & cities each touches 2-3 hexes)
+
54 * (1/3)linked by up to 3
________

72 edges ( roads: connects 2 vertices)

each edge has exactly 2 endpoint vertices
vertex.neighbors = adjacent vertices (distance rule enforcement)
"""

from maps.classic_catan_map import ClassicMap
from core.board import Board
from maps.spread_generation.map_spread_generator import MapSpreadGenerator
from shared.enums import Terrain


def setup_game() -> Board:
    
    m1 = ClassicMap()
    board = Board(m1)
    map_gen = MapSpreadGenerator(board)
    
    map_gen.generate()
    
    return board


b = setup_game()



resource_hexes = [h for h in b.hexes if h.terrain not in [Terrain.SEA, Terrain.DESERT]]

border_hexes = [
    h for h
    in resource_hexes
    if any(h.terrain == Terrain.SEA
            for h in h.adjacent_hexes)
]

for h in border_hexes:
    print(h)

print(len(border_hexes))


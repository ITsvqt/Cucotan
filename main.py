

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
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / 'src'))


from src.engine.game import Game
from enums import Terrain, PlayerColor




game = Game([PlayerColor.RED, PlayerColor.BLUE])

for h in game._board.hexes:
    print(h)



#* Test generate numbers
# b.hexes

# resource_hexes = [h for h in b.hexes if h.terrain not in [Terrain.SEA, Terrain.DESERT]]

# for h in b.hexes:
#     print(h)

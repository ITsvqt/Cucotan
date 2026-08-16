

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

# for id,cord in enumerate(sorted(ClassicMap._SEA_HEXES_CORDINATES, key=lambda x: (x[0],x[1])), 1):
#     print(f"{id} {cord}")
m1 = ClassicMap()
board = Board(m1)

print(f"hexes      :{len(board._hexes)}")
print(f"vertices   :{len(board._vertices)}")
print(f"edges      :{len(board._edges)}")


print(m1)

for id,v in board._vertices.items():
    print(f"{id}[{v.vertex_id} {len(v.adjacent_vertices)}]")
    print(f"{id}[{v.vertex_id} {len(v.adjacent_edges)}]")
    print()
        
        


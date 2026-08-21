from core.board import Board
from maps.base_map import base_map
from maps.classic_catan_map import ClassicMap

m1 = ClassicMap()
board = Board(m1)

#* Test terminal map repr
# print(m1)


#* Test cnt_generated_underlaying_game_objects
# print(f"hexes      :{len(board._hexes)}")
# print(f"vertices   :{len(board._vertices)}")
# print(f"edges      :{len(board._edges)}")


#* Test cnt_expected_vertices_links
# for id,v in board._vertices.items():
#     print(f"[{v.vertex_id}] {len(v.adjacent_vertices)} vertices")
#     print(f"[{v.vertex_id}] {len(v.adjacent_edges)} edges")
#     print()
        
#* Test board.wirte_hexes_neighbours()  result

# for h in b.hexes:
#     print(h)
#     for i, n in enumerate(h.adjacent_hexes):
#         print(f"\t[{i}]{n}")


#* Test generate_terrains sets map land hexes  terrain attirbute
# for hex in b.hexes:
#     print(hex)


#* Test generate_ports sets sea hexes and land vertices port attribute
#? manually tested the change of correct hex and vertex attributes
# for h in b.hexes:
#     print(h)

# for vertex in b._vertices.values():
#     print(vertex)

#* Test filter of resource hexes
# resource_hexes = [h for h in b.hexes if h.terrain not in [Terrain.SEA, Terrain.DESERT]]
# for r in resource_hexes:
#     print(r)

#* Test if any hex terrain is None
# none_hexes = [h for h in b.hexes if h.terrain is None]
# for r in none_hexes:
#     print(r)

#* Test get get hex by cordinates when valid data
# print(b.get_hex_by_cordinates(0,0))

#* Test get get hex by cordinates raise error when cordinates missing
# print(b.get_hex_by_cordinates(-4,-5))
    
        
#* Test generate dict with count of each key

# numbers = b.game_map.number_pool

# num_count = {}
# for num in numbers:
#     if num in num_count:
#         num_count[num] += 1
#     else:
#         num_count[num] = 1
        
# print(num_count)
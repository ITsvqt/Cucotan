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
        
#* Test get_hex_neigbours result
# land, sea = board.get_hex_neighoburs((-2,2))
# for i, l in enumerate(land):
#     print(f"l[{i}]: {l.q} {l.r}")

# for i, s in enumerate(sea):
#     print(f"s[{i}]: {s.q} {s.r}")
        
    
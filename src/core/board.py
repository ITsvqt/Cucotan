from core.hex import Hex
from core.vertex import Vertex
from core.edge import Edge
from typing import TYPE_CHECKING
from shared.enums import Terrain

if TYPE_CHECKING:
    from maps.base_map.base_map import BaseMap

# commit msg after completoing board
# Board model(orchestrator) completed

# 95 Resource Cards: 19 each of Brick, Grain, Lumber, Ore, and Wool
# 25 Development Cards: 14 Knights/Soldiers, 6 Progress Cards, and 5 Victory Point Cards.
# Player Pieces (in 4 colors): 16 cities (churches), 20 settlements (houses), and 60 roads (bars).
# Miscellaneous: 2 dice (1 red, 1 yellow), 1 robber, 2 Special Cards ("Longest Road" and "Largest Army"), and 4 "Building Costs" reference cards.


class Board:
    
    """ Responsible for constructing and wiring game objects. """
    
    _INIT_ERROR_KEY = "[On board init]"
    
    DIRECTIONS = [
        (0, -1),  # top-left
        (1, -1),  # top-right
        (-1, 0),  # left
        (1, 0),  # right
        (-1, 1),  # bottom-left
        (0, 1)  # bottom-right
        ]
    
    CORNER_NEIGHBORS = [
        # directions indecies
        (0, 1),  # corner 0: top
        (1, 3),  # corner 1: top-right
        (3, 5),  # corner 2: bottom-right
        (5, 4),  # corner 3: bottom
        (4, 2),  # corner 4: bottom-left
        (2, 0)   # corner 5: top-left
        ]
                # corner indecies
    EDGE_PAIRS = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,0)]

    
    def __init__(self, game_map: BaseMap):
        
        self._game_map = game_map
        
        self._hexes:    dict[int, Hex] = {}
        self._vertices: dict[int, Vertex] = {}
        self._edges:    dict[int, Edge] = {}
        self._hex_map:  dict[tuple[int, int], Hex] = {}  # (q, r) Hex for neigbor lookup
        self._corner_map: dict[frozenset, Vertex] = {}
        self._edge_map:   dict[frozenset, Edge]   = {}
        
        self._build()
        
        self._ensure_valid_build()

        # Board generation
        # self._hexes: list[Hex] = self._create_hexes(land_hexes_cordinates)
    
    def _build(self):
        self._create_hexes()
        self._create_vertices_and_edges()
        self._wire_all()
    
    def _create_hexes(self):
  
        for hex_id, land_cordinates in enumerate(
            self._game_map.land_hexes_cordinates
            ):
            q, r = land_cordinates
            new_hex = Hex(hex_id, q, r)
            self._hexes[hex_id] = new_hex
            self._hex_map[(q, r)] = new_hex
        
        next_hex_id = len(self._hexes)
        
        for hex_id, sea_cordinates in enumerate(
            self._game_map.sea_hexes_cordinates,
            start=next_hex_id
            ):
            q, r = sea_cordinates
            new_hex = Hex(hex_id, q, r, Terrain.SEA)
            self._hexes[hex_id] = new_hex
            self._hex_map[(q, r)] = new_hex
            
    def _create_vertices_and_edges(self):
        vertex_id = 0
        edge_id = 0
        
        corner_map: dict[frozenset, Vertex] = {}
        edge_map  : dict[frozenset, Edge  ] = {}

        land_hexes = [self._hex_map[coords] for coords in self._game_map.land_hexes_cordinates]
        for hex in land_hexes:
            q, r = hex.q, hex.r
            
            hex_corners: list[Vertex] = []
            for dir_a, dir_b in self.CORNER_NEIGHBORS:
                dqa, dra = self.DIRECTIONS[dir_a]
                dqb, drb = self.DIRECTIONS[dir_b]
                
                # 3 hex cordinates that meet at that corner
                key = frozenset([(q, r), (q+dqa, r+dra), (q+dqb, r+drb)])

                if key not in corner_map:
                    v = Vertex(vertex_id)
                    corner_map[key] = v
                    self._vertices[vertex_id] = v
                    vertex_id += 1

                hex_corners.append(corner_map[key])
            
            for i, j in self.EDGE_PAIRS:
                v1, v2 = hex_corners[i], hex_corners[j]
                key = frozenset([v1.vertex_id, v2.vertex_id])

                if key not in edge_map:
                    e = Edge(edge_id)
                    edge_map[key] = e
                    self._edges[edge_id] = e
                    edge_id += 1
                    
        self._corner_map = corner_map
        self._edge_map = edge_map
                    
    def _wire_all(self):
        pass
            

            
        
            
            
            
    def _ensure_valid_build(self):
        loctn_msg = self._INIT_ERROR_KEY
        if len(self._hexes) != self._game_map.cnt_hex:
            raise ValueError(
                f"{loctn_msg} Hex count generation missmatch!\n"
                f"Exp : [{self._game_map.cnt_hex}]\n"
                f"Actl: [{len(self._hexes)}]"
            )
        if len(self._vertices) != self._game_map.cnt_vertex:
            raise ValueError(
                f"{loctn_msg} Vertex count generation missmatch!\n"
                f"Exp : [{self._game_map.cnt_vertex}]\n"
                f"Actl: [{len(self._vertices)}]"
            )
        if len(self._edges) != self._game_map.cnt_edge:
            raise ValueError(
                f"{loctn_msg} Edge count generation missmatch!\n"
                f"Exp : [{self._game_map.cnt_edge}]\n"
                f"Actl: [{len(self._edges)}]"
            )
    
    # def _build(self):
    #     layout = MapGenerator(self._game_map).generate()
    #     self._create_hexes(layout)
    
    
    
    
    
    
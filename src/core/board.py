
from __future__ import annotations
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
        # 2D directions for the hex grid
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
        
        self._hexes:    dict[int, Hex] = {}     # fast lookup for the state layer
        self._vertices: dict[int, Vertex] = {}
        self._edges:    dict[int, Edge] = {}
        
        self._hex_map:  dict[tuple[int, int], Hex] = {}  # key: cords of the hex
        
        # this is used only by map generator to apply game's Port logic
        # (after randomization) to  Hex and Vertex
        self._ports_hex_and_vertices_effect: list[tuple[Hex, Vertex, Vertex]] = [] 
        
        
        self._build()
        self._ensure_valid_build() # small validation
        
    
    @property
    def game_map(self) -> BaseMap:
        return self._game_map
    
    @property
    def hexes(self) -> tuple[Hex]:
        return tuple(self._hexes.values())
        
    @property
    def land_hexes(self) -> tuple[Hex]:
        return tuple(self._hex_map[h] for h in self._game_map.land_hexes_cordinates)
    
    @property
    def ports_effect(self):
        return self._ports_hex_and_vertices_effect
    

    def get_hex_by_cordinates(self, q: int, r: int):
        if (q,r) not in self._hex_map:
            raise ValueError(f"[get hex with cordinates] Hex cordinates({q}, {r}) can't be found in the board!")
        
        return self._hex_map[(q,r)]
        
        
        
    def get_hex_neighoburs(self, hex_cords: tuple[int, int]) -> tuple[tuple[Hex], tuple[Hex]]:
        """ Should be called for a land hex\n
            param[0]: Target hex cordinates\n
            Returns: neighour land and sea neigbour hexes separated in 2 tuples"""
            
        land_hexes = []
        sea_hexes = []
        
        for dir in self.DIRECTIONS:
            neighobur_cords = (hex_cords[0] + dir[0], hex_cords[1] + dir[1])
            
            try:
                curr = self._hex_map[neighobur_cords]
            except:
                raise ValueError(f"Invalid land hex cords param: {hex_cords} ")
            
            if neighobur_cords in self._game_map.land_hexes_cordinates:
                land_hexes.append(curr)
            else:
                sea_hexes.append(curr)
            
        return (tuple(land_hexes), tuple(sea_hexes))
    
    


    
    def _build(self):
        self._create_hexes()
        corner_map = self._create_vertices_and_edges()
        self._wire_edges()
        self._create_ports(corner_map)
    
    
    def _create_hexes(self):
        """ Generated ids in self._hexes in order of processing land & sea hex cordinates,
        ensures slicing to """    
  
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
        
        """ Both in the same function, because they rely on the same hex logic.
            This method also wires the created vertices and edges to their belonging hex.
            Wires hexes,edge, and adjacent vertices to their vertices.
            Wires vertices the edge connects."""
            
        vertex_id = 0
        edge_id = 0
        
        # data to check for deduplication
        corner_map: dict[frozenset, Vertex] = {}  # key: cords of 3 hexes the vertex is on
        edge_map  : dict[frozenset, Edge  ] = {}  # key: ids of 2 vertices the edge connects
        
        # save adjacent on creation to wire at the end
        vertex_adj_vertices: dict[int, list[Vertex]] = {}
        vertex_adj_edges   : dict[int, list[Edge]]   = {}

        land_hexes = [self._hex_map[coords] for coords in self._game_map.land_hexes_cordinates]
        for hex in land_hexes:
            q, r = hex.q, hex.r
            
            # save each vertex to create edges between them
            # even if not created (map saves already created edges between vertices)
            hex_corners: list[Vertex] = []
            #* CREATING VERTICES
            for dir_a, dir_b in self.CORNER_NEIGHBORS:
                dqa, dra = self.DIRECTIONS[dir_a]
                dqb, drb = self.DIRECTIONS[dir_b]
                
                # 3 hex cordinates that meet at that corner
                key = frozenset([(q, r), (q+dqa, r+dra), (q+dqb, r+drb)])

                if key not in corner_map:
                    v = Vertex(vertex_id)
                    corner_map[key] = v
                    self._vertices[vertex_id] = v
                    vertex_adj_vertices[vertex_id] = []
                    vertex_adj_edges[vertex_id] = []
                    v.wire_hexes(tuple(self._hex_map[coords] for coords in key))
                    vertex_id += 1

                # unique key for each vertex (the cordinates of 3 hexes it is on)
                hex_corners.append(corner_map[key])
            
            # save each edges to wire them with the hex
            # even if not created (creation is unique, referencing them is duplicate within hexes)
            hex_edges = []
            #* CREATING EDGES
            for i, j in self.EDGE_PAIRS:
                v1, v2 = hex_corners[i], hex_corners[j]
                
                # 2 vertices that edge connect
                key = frozenset([v1.vertex_id, v2.vertex_id])

                if key not in edge_map:
                    e = Edge(edge_id)
                    edge_map[key] = e
                    self._edges[edge_id] = e
                    vertex_adj_vertices[v1.vertex_id].append(v2)
                    vertex_adj_vertices[v2.vertex_id].append(v1)
                    vertex_adj_edges[v1.vertex_id].append(e)
                    vertex_adj_edges[v2.vertex_id].append(e)
                    e.wire_vertices(tuple((v1,v2)))
                    edge_id += 1
                hex_edges.append(edge_map[key])
            
            # wire the hex on the spot
            # since it doesn't require future iterations like vertices and edges
            hex.wire(tuple(hex_corners), tuple(hex_edges))
            
        for vertex in self._vertices.values():
            vertex.wire_vertices(tuple(vertex_adj_vertices[vertex.vertex_id]))
            vertex.wire_edges(tuple(vertex_adj_edges[vertex.vertex_id]))
            
        return corner_map
                
                    
    def _wire_edges(self):
        """ Wire hexes and edges last, because they depend on creating and wiring hexes and vertices. """
        
        for edge in self._edges.values():
            v1, v2 = edge.adjacent_vertices
            
            adj_hexes = tuple(h for h in v1.adjacent_hexes if h in v2.adjacent_hexes)
            edge.wire_hexes(adj_hexes)
            
            adj_edges = tuple(
                e for e in (set(v1.adjacent_edges) | set(v2.adjacent_edges))
                if e is not edge
            )
            edge.wire_edges(adj_edges)
            
            
    def _create_ports(self, corner_map: dict[frozenset, Vertex]):
        """ Prepare collection of hex and vertices for each port,
        to be set by map spread generator. """
        
        for cords_direction in self._game_map.ports_cords_and_direction:
            
            coords, directions = cords_direction
            land_coords = (coords[0] + directions[0], coords[1] + directions[1])
            sea_hex = self._hex_map[coords]
            
            docking_vertices = [
                v for key, v in corner_map.items()
                if coords in key and land_coords in key
                ]
            
            self._ports_hex_and_vertices_effect.append((sea_hex, *docking_vertices))
            
            
        
   
    # VALIDATION METHODS       
    def _ensure_valid_build(self):
        """ Compares count of generated hex,vertex, and edge against the human calculated expected amount. """
        
        
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
        if len(self._ports_hex_and_vertices_effect) != self._game_map.cnt_port:
            raise ValueError(
                f"{loctn_msg} Port Type generation data missmatch!\n"
                f"Exp : [{self._game_map.cnt_port}]\n"
                f"Actl: [{len(self._ports_hex_and_vertices_effect)}]"
            )
        
        for i in range(len(self._ports_hex_and_vertices_effect)):
            port_data = self._ports_hex_and_vertices_effect[i]
            if len(port_data) != 3:
                raise ValueError(
                    f"{loctn_msg} Port data at index [{i}] malformed!\n"
                    f"Exp : [3] Hex Vertex Vertex\n"
                    f"Actl: {len(port_data)}"
                )    
            
        
    
    
    
    
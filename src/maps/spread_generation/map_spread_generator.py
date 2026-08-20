from __future__ import annotations
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from core.board import Board
    from shared.enums import Terrain, PortType




"""
Swap Generators on the Fly: You can create an abstract base class or protocol MapGenerator in your game-logic module.
Then implement StandardMapGenerator, DesertOnlyGenerator, or RandomClusterGenerator.
Your game initialization code just picks whichever generator the player chose in the settings menu and passes board to it.
"""


class MapSpreadGenerator:
    
    """ 
    This implementation is the most competitive for game runs and is designed for the classic map. 
    (because of symetric corners definition in map AND actual dependency on [2,12] being present once in the numbers list)
    
    Generates a valid random distribution of game resources, based on the original game rules.
    MapGenerator accepts board obj.
    Call generate() method to run everything.
    """
    
    # BALANCED HEX NUMBER DISTRIBUTION
    
    def __init__(self, board: Board, seed = None):
        """ Uses the seed-based generator to produce identical results for identical seeds. """
        
        self._board = board
        self._rng = random.Random(seed)
    
    
    _PIP_VALUES = {2:1, 3:2, 4:3, 5:4, 6:5, 8:5, 9:4, 10:3, 11:2, 12:1}
    _PIP_GROUPS = [[6,8], [5,9], [4,10], [3,11]]
    _MAX_RETRIES = 100
    _MAX_PIP_PER_VERTEX = 13
    
    
    def generate(self):
        self._generate_terrains()
        self._generate_ports()
        # number_map = self._assign_numbers(terrain_map)
        
    
    
    def _generate_terrains(self):
        """ Randomize terrain spread across the map's hexes. """

        terrain_pool = self._board._game_map.terrain_pool.copy()
        random.shuffle(terrain_pool)
        random.shuffle(terrain_pool)
        
        for i in range(len(terrain_pool)):
            self._board.land_hexes[i].terrain = terrain_pool[i]
            
            
    def _generate_ports(self):
        """ Randomize port type spread across the map's ports. """

        port_pool = self._board.game_map.port_pool.copy()
        random.shuffle(port_pool)
        random.shuffle(port_pool)
        
        for i in range(len(port_pool)):
            for el in self._board.ports_effect[i]:
                el.port = port_pool[i]
                
                
    def _generate_numbers(self):
        """ Randomize numbers spread across the map's hexes.
        place_pip1_numbers"""
        
        numbers = self._board.game_map.number_pool
        resource_hexes = [h for h in self._board.hexes if h.terrain not in [Terrain.SEA, Terrain.DESERT]]
        
        self._ensure_numbers_and_resource_hexes_cnt_match(numbers, resource_hexes)
        
        num_count = {}
        for num in numbers:
            if num in num_count:
                num_count[num] += 1
            else:
                num_count[num] = 1
                
        assigned = self._place_pip1_numbers(num_count)
        
    
    def _place_pip1_numbers(self, num_count) -> dict:
        """ Stongly depends on 2 and 12 numbers being present only once on the map."""
        
        assigned = {}
        combos = self._board.game_map.symetric_corner_hexes
        
        if combos:
            pair = random.choice(combos)
                            
        
        return assigned
        
    
    def _ensure_numbers_and_resource_hexes_cnt_match(self, numbers, resource_hexes):
        
        if len(numbers) != len(resource_hexes):
            raise ValueError(
                f"[numbers generation] Unsimetric data.\n"
                f"cnt_numbers: {len(numbers)}\n"
                f"cnt_hex    : {len(resource_hexes)}"
                )
        
                
        
        
        
        

        
    
    def _assign_numbers(
        self,
        terrain_map: dict[tuple[int, int], Terrain]
        ) -> dict[tuple[int, int], int]:
        """ Randomize number spread across resource hexes. """

        number_pool = self._game_map.number_pool.copy()
        random.shuffle(number_pool)
        positions = [  # non-desert positions (already shuffled)
            pos 
            for pos, terrain 
            in terrain_map.items()
            if terrain != Terrain.DESERT 
            ]
        
        remaining = {pos: number_pool.copy() for pos in positions}
        assigned = {}
        
        i = 0
        while i < len(positions):
            pos = positions[i]

            placed = False
            while remaining[pos]:
                candidate = remaining[pos].pop()
                if is_valid(pos, candidate, assigned):
                    assigned[pos] = candidate
                    placed = True
                    break
            if placed == True:
                i += 1
            else:  # backtrack
                del assigned[pos]
                remaining[pos] = number_pool.copy() # reset
                i -= 1
                
                if i < 0:
                    # full restart
                    random.shuffle(number_pool)
                    remaining = {pos: number_pool.copy() for pos in positions}
                    i = 0
            
            
            
            
    
    def _assign_ports():
        """ Randomize port spread across sea hexes. """
        pass
    
    
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
    
    """ Generates a valid random distribution of game resources, based on the original game rules.
    MapGenerator accepts board obj.
    Call generate() method to run everything.
    """
    
    # BALANCED HEX NUMBER DISTRIBUTION
    
    def __init__(self, board: Board, seed = None):
        """ Uses the seed-based generator to produce identical results for identical seeds. """
        
        self._board = board
        self._rng = random.Random(seed)
    
    
    PIP_VALUES = {2:1, 3:2, 4:3, 5:4, 6:5, 8:5, 9:4, 10:3, 11:2, 12:1}
    PIP_GROUPS = [[6,8], [5,9], [4,10], [3,11], [2,12]]
    MAX_RETRIES = 100
    MAX_PIP_PER_VERTEX = 13
    
    
    def generate(self):
        self._generate_terrains()
        # number_map = self._assign_numbers(terrain_map)
        # port_map = self._assign_ports()
        
    
    
    def _generate_terrains(self) -> dict[tuple[int,int], Terrain]:
        """ Randomize resource spread across the map. """

        terrain_pool = self._board._game_map.terrain_pool.copy()
        random.shuffle(terrain_pool)
        random.shuffle(terrain_pool)
        
        for i in range(len(terrain_pool)):
            
            self._board.land_hexes[i].terrain = terrain_pool[i]
        
    
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
    
    
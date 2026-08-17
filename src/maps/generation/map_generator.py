from __future__ import annotations
from typing import TYPE_CHECKING
import random
from maps.generation.map_layout import MapLayout
if TYPE_CHECKING:
    from maps.base_map.base_map import BaseMap
    from shared.enums import Terrain, PortType



class MapGenerator:
    
    """ Generates random map layout from predefined map data. """
    
    # BALANCED HEX NUMBER DISTRIBUTION
    MAX_DOTS_PER_VERTEX = 13
    
    def __init__(self, game_map: BaseMap):
        self._game_map = game_map
    
    
    def generate(self):
        terrain_map = self._assign_terrains()
        number_map = self._assign_numbers(terrain_map)
        port_map = self._assign_ports()
        
        return MapLayout(terrain_map)
    
    
    def _assign_terrains(self) -> dict[tuple[int,int], Terrain]:
        """ Randomize resource spread across the map. """

        land_hexes_cordinates = self._game_map.land_hexes_cordinates
        terrain_pool = self._game_map.terrain_pool.copy()
        random.shuffle(terrain_pool)
        
        #? zipping a set(land_hexes_cordinates)
        #? which is unordered ( extra bit of randomness )
        return dict(zip(land_hexes_cordinates, terrain_pool))
        
        
    
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
    
    
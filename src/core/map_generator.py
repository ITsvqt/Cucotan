
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from maps.base_map.base_map import BaseMap


class MapGenerator:
    
    def __init__(self, game_map: BaseMap):
        self._game_map = game_map
    
    
    def generate(self):
        pass
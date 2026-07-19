from typing import NamedTuple
from shared.enums import Terrain, PortType


class MapLayout(NamedTuple):
    
    """ Data container. Holds the result of map's data randomization. """
    
    # terrain map : which terrain on which hex
    terrain_map: dict[tuple[int, int], Terrain]
    # number map  : which number on which hex
    number_map : dict[tuple[int, int], int]
    # port map: which port on which sea hex
    port_map   : dict[tuple[int, int], PortType]

        
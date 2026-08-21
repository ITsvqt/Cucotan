
from maps.base_map.base_map import BaseMap
from shared.enums import Terrain, PortType

class ClassicMap(BaseMap):
    
    """ Original base map of Catan. """
    
    # CONSTANTS
      # LAND
    _CNT_FOREST   = 4  # wood
    _CNT_PASTURE  = 4  # sheep
    _CNT_FIELDS   = 4  # wheat
    _CNT_MOUNTAIN = 3  # ore
    _CNT_HILLS    = 3  # brick
    _CNT_DESERT   = 1  # no resource
    _CNT_LAND_HEX = 19 # expected to match the sum of all different land tiles
    _LAND_HEXES_CORDINATES = {
                (0,-2),( 1,-2),(2,-2),
            (-1,-1),(0,-1),(1,-1),(2,-1),
        (-2, 0),(-1, 0),(0, 0),(1, 0),(2,0),
            (-2, 1),(-1, 1),(0, 1),(1, 1),
                (-2, 2),( -1, 2),(0, 2)
    }
    _TERRAIN_POOL = (
        [Terrain.FOREST]     * _CNT_FOREST
        + [Terrain.PASTURE]  * _CNT_PASTURE
        + [Terrain.FIELD]    * _CNT_FIELDS
        + [Terrain.HILL]     * _CNT_HILLS
        + [Terrain.MOUNTAIN] * _CNT_MOUNTAIN
        + [Terrain.DESERT]   * _CNT_DESERT
        )
    
      # NUMBERS
    _CNT_NUMBER = _CNT_LAND_HEX - _CNT_DESERT 
    _NUMBERS_POOL = (
        [3, 4, 5, 6, 8, 9, 10, 11] * 2
        + [2, 12] * 1
    )
    
    _SYMETRIC_CORNERS = {
        # To balance 2, 12 dice numbers
        ((0, -2), (0, 2)),
        ((1, -2), (-1, 2)),
        ((2, -2), (-2, 2)),
        ((2, -1), (-2, 1)),
        ((2, 0), (-2, 0)),
        ((1, 1), (-1, -1))
    }
    
      # SEA
    _CNT_SEA_HEX = 18
    _SEA_HEXES_CORDINATES = {
            (0,-3),(1,-3),(2,-3),(3,-3),
          (-1,-2),                  (3,-2),
        (-2, -1),                    (3, -1),
       (-3, 0),                        (3, 0),
         (-3, 1),                    (2, 1),
          (-3, 2),                  (1, 2),
            (-3,3),(-2,3),(-1,3),(0,3)
    }
    
      # PORTS
    CNT_GENERIC_PORT = 4
    CNT_PORT_PER_RESOUCE = 1
    _CNT_PORT     = 9  # 4 generic + 1 for each resource
    _PORTS_CORDINATES_AND_DIRECTION = { # t1: hex cord, t2: facing dir
           ((0, -3), (0, 1)), ((2, -3), (-1, 1)),
                                 ((3, -2), (-1, 1)),
        ((-2, -1), (1, 0)),
                                     ((3, 0), (-1, 0)),
        ((-3, 1), (1, 0)),
                                 ((1, 2), (0, -1)),
           ((-3, 3), (1, -1)), ((-1, 3), (0, -1))
    }
    
    _PORTS_POOL = (
        [PortType.GENERIC] * CNT_GENERIC_PORT
        + [PortType.CLAY] * CNT_PORT_PER_RESOUCE
        + [PortType.WOOD] * CNT_PORT_PER_RESOUCE
        + [PortType.SHEEP] * CNT_PORT_PER_RESOUCE
        + [PortType.GRAIN] * CNT_PORT_PER_RESOUCE
        + [PortType.ORE] * CNT_PORT_PER_RESOUCE
    )
    
      # GENERATION VALIDATION
    _CNT_HEX = _CNT_LAND_HEX + _CNT_SEA_HEX # 37
    _CNT_VERTEX = 54
    _CNT_EDGE = 72  
    
    def __init__(self):
        super().__init__(
            self._CNT_LAND_HEX,
            self._LAND_HEXES_CORDINATES,
            self._TERRAIN_POOL,
            self._CNT_NUMBER,
            self._NUMBERS_POOL,
            self._CNT_SEA_HEX,
            self._SEA_HEXES_CORDINATES,
            self._CNT_PORT,
            self._PORTS_CORDINATES_AND_DIRECTION,
            self._PORTS_POOL,
            self._CNT_HEX,
            self._CNT_VERTEX,
            self._CNT_EDGE,
            self._SYMETRIC_CORNERS
        )
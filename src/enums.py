from enum import Enum, auto

"""
    This is the language for custom types.
    Everyting the static game data and dynamic game state data will speak.
"""


class Terrain(Enum):
    """ The seven terrain types a hex can be. """
    
    HILL     = 'Hill'     # clay
    FOREST   = 'Forest'   # wood
    PASTURE  = 'Pasture'  # sheep
    FIELD    = 'Field'    # wheat
    MOUNTAIN = 'Mountain' # ore
    DESERT   = 'Desert'   # none
    SEA      = 'Sea'      # none
    
class Resource(Enum):
    """ The five tradeable resources in the game. """
    CLAY     = 'Clay'
    WOOD     = 'Wood'
    SHEEP    = 'Sheep'
    GRAIN    = 'Grain'
    ORE      = 'Ore'
    
class PortType(Enum):
    """ Port trade ratios available on the board edge. """
    CLAY     = 'Clay'  # auto():auto()
    WOOD     = 'Wood'  # auto():auto()
    SHEEP    = 'Sheep'  # auto():auto()
    GRAIN    = 'Grain'  # auto():auto()
    ORE      = 'Ore'  # auto():auto()
    GENERIC  = 'Generic'  # auto():auto()


class BuildingType(Enum):
    """ What can be placed on a vertex. """
    SETTLEMENT = 'Settlement'
    CITY       = 'City'
    
class GamePhase(Enum):
    """ Top-level phases the game engine moves through. """
    SETUP_FORWARD  = auto()   # placement round auto() (first player → last)
    SETUP_BACKWARD = auto()   # placement round auto() (last player → first)
    MAIN           = auto()   # normal turns
    ENDED          = auto()
    
    
# ---* Lookup tables (not enums, but live here as they are static/shared) *---

TERRAIN_TO_RESOURCE: dict[Terrain, Resource | None] = {
    Terrain.FOREST:   Resource.WOOD,
    Terrain.PASTURE:  Resource.SHEEP,
    Terrain.FIELD:    Resource.GRAIN,
    Terrain.HILL:     Resource.CLAY,
    Terrain.MOUNTAIN: Resource.ORE
}


PORT_TO_RESOURCE: dict[PortType, Resource | None] = {
    PortType.GENERIC: None,
    PortType.WOOD:    Resource.WOOD,
    PortType.SHEEP:   Resource.SHEEP,
    PortType.GRAIN:   Resource.GRAIN,
    PortType.CLAY:    Resource.CLAY,
    PortType.ORE:     Resource.ORE,
}



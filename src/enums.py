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

    
class GamePhase(Enum):
    """ Top-level phases the game engine moves through. """
    SETUP_FORWARD  = auto()   # placement round auto() (first player → last)
    SETUP_BACKWARD = auto()   # placement round auto() (last player → first)
    MAIN           = auto()   # normal turns
    ENDED          = auto()
    
    
class TurnSubPhase(Enum):
    PRE_ROLL  = auto()   # player must roll (or play a knight/road-building before)
    POST_ROLL = auto()   # player may build/trade/play dev cards, then end turn


class DevCard(Enum):
    KNIGHT         = auto()
    ROAD_BUILDING  = auto()
    YEAR_OF_PLENTY = auto()
    MONOPOLY       = auto()
    VICTORY_POINT  = auto()
    
class PlayerColor(Enum):
    RED    = auto()
    GREEN  = auto()
    BLUE   = auto()
    YELLOW = auto()
    
#* Lookup tables (not enums, but live here as they are static/shared)

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



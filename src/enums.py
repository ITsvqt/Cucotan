from enum import Enum, auto


class Terrain(Enum):
    """ The seven terrain types a hex can """
    
    HILL     = auto()
    FOREST   = auto()
    PASTURE  = auto()
    FIELD    = auto()
    MOUNTAIN = auto()
    DESERT  = auto()
    SEA      = auto()
    
class Resource(Enum):
    """ The five tradeable resources in the game. """
    CLAY    = auto()
    WOOD   = auto()
    SHEEP    = auto()
    GRAIN    = auto()
    ORE      = auto()
    
class PortType(Enum):
    """ Port trade ratios available on the board edge. """
    CLAY    = auto()  # auto():auto()
    WOOD   = auto()  # auto():auto()
    SHEEP    = auto()  # auto():auto()
    GRAIN    = auto()  # auto():auto()
    ORE      = auto()  # auto():auto()
    GENERIC  = auto()  # auto():auto()


class BuildingType(Enum):
    """ What can be placed on a vertex. """
    SETTLEMENT = auto()
    CITY       = auto()
    
class GamePhase(Enum):
    """Top-level phases the game engine moves through."""
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



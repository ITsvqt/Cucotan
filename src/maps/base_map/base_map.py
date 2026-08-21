from __future__ import annotations

from typing import TYPE_CHECKING
from shared.enums import Terrain

if TYPE_CHECKING:
    from shared.enums import PortType

class BaseMap:
    
    """
        Base class for all map layouts.
        Derrived classes store base class required attributes for concrete map
        as precalculated by human constants. Parrent provides validation for the length of the lists.
        
        Map generation relies on randomly consuming entries from predefined data lists without repetition.
    """
    
    
    _INIT_ERROR_KEY = "[On map init]"
    

    def __init__(
        self,
        
        # RESOURCE HEXES DATA
        cnt_land_hex  : int,                            # count of land tiles
        land_hexes_cordinates: set[ tuple[int, int] ],  # coordinates of each land tile
        terrain_pool  : list[ Terrain ],                # 1 desert, 3 mountains, 3 mines, 4 pastures ...
        cnt_resource_number    : int,                   # count of numbers for resource tiles
        number_pool   : list[ int ],                    # 1x12, 2x8 ...
        
        # SEA HEXES DATA
        cnt_sea_hex   : int,                            # count of sea tiles
        sea_hexes_cordinates : set[ tuple[int, int] ],  # coordinates of each sea_hex
        
        # ADDITIONAL GAME DATA
        cnt_port      : int,                            # count of ports
        ports_cords_and_direction: set[tuple, tuple],   # t1: hex_cord, t2: facing direction 
        ports_pool     : list[ PortType ],              # 3x3:1, 1xwheat(2:1)
        
        # VALUES FOR VALIDATING DATA VOLUME
        cnt_hex       : int,                            # for validation of generated data
        cnt_vertex    : int,                            # for validation of generated data
        cnt_edge      : int,                            # for validation of generated data
        
        # SYMETRIC CORNERS HEXES FOR LOWEST PIP DISTRIBUTION
        symetric_pip1_combinations: set[tuple[tuple, tuple]] = None
        ):
        
        self._ensure_hex_data_lengths_match(
            cnt_land_hex, land_hexes_cordinates, terrain_pool,
            cnt_resource_number, number_pool,
            cnt_sea_hex, sea_hexes_cordinates
            )
        self._ensure_port_data_length_match(cnt_port, ports_cords_and_direction, ports_pool)
        self._ensure_land_and_sea_hexes_do_not_overlap(land_hexes_cordinates, sea_hexes_cordinates)
        self._ensure_valid_port_data(land_hexes_cordinates, sea_hexes_cordinates, ports_cords_and_direction)
        self._ensure_valid_dice_number_pool(number_pool)
        
        # Land
        self._cnt_land_hex = cnt_land_hex
        self._land_hexes_cordinates = land_hexes_cordinates
        self._terrain_pool = terrain_pool
        self._number_pool = number_pool
        
        # Sea
        self._cnt_sea_hex = cnt_sea_hex
        self._sea_hexes_cordinates = sea_hexes_cordinates
        
        # Port
        self._cnt_port = cnt_port
        self._ports_cords_and_direction = ports_cords_and_direction
        self._port_pool = ports_pool
        
        # Expected values for generation
        self._cnt_hexes = cnt_hex
        self._cnt_vertex = cnt_vertex
        self._cnt_edge = cnt_edge
        
        # Symetric corner hexes
        self._symetric_corner_hexes = symetric_pip1_combinations
        
        
        
    # DUNDER
    def __str__(self):
        result = []
        result.append(f"Map: {type(self).__name__}")
        result.append(f"Cnt_land: {self._cnt_land_hex}")
        result.append(self._map_hexes_as_string(
                        self._land_hexes_cordinates,
                        self._sea_hexes_cordinates
                    )
                )
        return '\n'.join(result)
            
            
    # PROPERTIES
    @property
    def terrain_pool(self):
        return self._terrain_pool
    
    @property
    def number_pool(self):
        return self._number_pool
    
    @property
    def land_hexes_cordinates(self):
        return self._land_hexes_cordinates
    
    @property
    def ports_cords_and_direction(self):
        return self._ports_cords_and_direction
    
    @property
    def port_pool(self):
        return self._port_pool
    
    @property
    def sea_hexes_cordinates(self):
        return self._sea_hexes_cordinates
    
    @property
    def hexes_cordinates(self):
        return self._land_hexes_cordinates | self._sea_hexes_cordinates
    
    @property
    def cnt_hex(self):
        return self._cnt_hexes
    
    @property
    def cnt_vertex(self):
        return self._cnt_vertex
    
    @property
    def cnt_edge(self):
        return self._cnt_edge
    
    @property
    def cnt_port(self):
        return self._cnt_port
    
    @property
    def symetric_corner_hexes(self):
        return self._symetric_corner_hexes
    

    # PRIVATE STATIC METHODS
    @ staticmethod
    def _map_hexes_as_string(land_hexes_cordinates, sea_hexes_cordinates) -> str:
        result = []
        
        all_hexes = land_hexes_cordinates | sea_hexes_cordinates

        min_r = min(r for _, r in all_hexes)
        max_r = max(r for _, r in all_hexes)

        for r in range(min_r, max_r + 1):
            # All q values that exist in this row
            qs = sorted(q for q, rr in all_hexes if rr == r)

            # One symbol ("@ " or "~ ") occupies 2 characters.
            line = " " * abs(r)

            for q in qs:
                if (q, r) in land_hexes_cordinates:
                    line += "@ "
                else:
                    line += "~ "
            result.append(line.rstrip())
        return '\n'.join(result)
    
      # INIT DATA VALIDATION METHODS
    @staticmethod
    def _ensure_hex_data_lengths_match(
        cnt_land_hex: int,
        land_hexes_cordinates: set[tuple[int, int]],
        terrain_pool: list[Terrain],
        cnt_number_pool: int,
        number_pool: list[int],
        cnt_sea_hex: int,
        sea_hexes_cordinates: set[tuple[int, int]]
        ):
        
        """ Checks collections of hexes data for mismatching length. """
        
        
        # expected cnt of land hex cordinates
        localization_msg = BaseMap._INIT_ERROR_KEY
        if cnt_land_hex != len(land_hexes_cordinates):
            raise ValueError(
                f"{localization_msg} Illegal land hexes coordinates count!\n"
                f"Exp : [{cnt_land_hex}]\n"
                f"Actl: [{len(land_hexes_cordinates)}]"
                )
        # expected cnt of land hex Terrain (Desert included)
        if cnt_land_hex != len(terrain_pool):
            raise ValueError(
                f"{localization_msg} Illegal terrain pool count on map init!\n"
                f"Exp : [{cnt_land_hex}]\n"
                f"Actl: [{len(terrain_pool)}]"
            )
        # expected cnt of resource hex numbers
        if cnt_number_pool != len(number_pool):
            raise ValueError(
                f"{localization_msg} Illegal dice numbers for tarrain count!\n"
                f"Exp : [{cnt_number_pool}]\n"
                f"Actl: [{len(number_pool)}]"
            )
        # expected cnt of sea hex cordinates
        if cnt_sea_hex != len(sea_hexes_cordinates):
            raise ValueError(
                f"{localization_msg} Illegal sea hexes coordinates count!\n"
                f"Exp : [{cnt_sea_hex}]\n"
                f"Actl: [{len(sea_hexes_cordinates)}]"
                )
            
    @staticmethod    
    def _ensure_port_data_length_match(cnt_port: int, ports_cords_and_dir: set, ports_pool: list[PortType]): 
        """ Checks collections of ports data for mismatching length. """
        
        # expected cnt of port cordinates+direction
        if cnt_port != len(ports_cords_and_dir):
            raise ValueError(
                f"{BaseMap._INIT_ERROR_KEY} Illegal ports cordinates count\n"
                f"Exp: {cnt_port}\n"
                f"Actl: [{len(ports_cords_and_dir)}]"
            )
        
        # expected cnt of PortType
        if cnt_port != len(ports_pool):
            raise ValueError(
                f"{BaseMap._INIT_ERROR_KEY} Illegal ports counts\n"
                f"Exp: {cnt_port}\n"
                f"Actl: [{len(ports_pool)}]"
                )
            
            
    @staticmethod
    def _ensure_land_and_sea_hexes_do_not_overlap(land_hexes_cordinates:set, sea_hexes_cordinate:set):
        """ Checks if land and sea overlap. """

        overlap = land_hexes_cordinates.intersection(sea_hexes_cordinate) 
        if len(overlap) != 0:
            overlap_lines = [f"{cordinates}" for cordinates in overlap]
            raise ValueError(
                f"{BaseMap._INIT_ERROR_KEY} Land and sea hexes overlap at:\n"
                f"{'\n'.join(overlap_lines)}"
                )
    
    @staticmethod
    def _ensure_valid_port_data(land_hexes_cordinates: set, sea_hexes_cordinates: set, ports_cords_and_direction: set):
        """ Checks if ports cordinates are sea_hexes cordinates
        Checks if port cords + direction are valid land_hexes """
        
        ports_cords = set([x[0] for x in ports_cords_and_direction])
        
        difference = ports_cords.difference(sea_hexes_cordinates)
        if len(difference) != 0:
            difference_lines = [f"{cordinates}" for cordinates in difference]
            raise ValueError(
                f"{BaseMap._INIT_ERROR_KEY} Port cordinates that are not on sea:\n"
                f"{'\n'.join(difference_lines)}"
            )
        
        ports_facing_land_cords = set([(x[0] + y[0], x[1] + y[1]) for x,y in [t for t in ports_cords_and_direction]])
        
        difference = ports_facing_land_cords.difference(land_hexes_cordinates)
        if len(difference) != 0:
            difference_lines = [f"{cordinates}" for cordinates in difference]
            raise ValueError(
                f"{BaseMap._INIT_ERROR_KEY} Port facing land is not in the map:\n"
                f"{'\n'.join(difference_lines)}"
            )
    
    
    @staticmethod
    def _ensure_valid_dice_number_pool(numbers_pool: list[int]):
        """ Checks values in the pool of numbers for terrain hexes. """
        
        valid_number_values = {2,3,4,5,6,8,9,10,11,12} # possible 2 dice rolls (except 7)
        
        for number in numbers_pool:
            if number not in valid_number_values:
                raise ValueError(f"{BaseMap._INIT_ERROR_KEY} Illegal number [{number}] in dice numbers pool!\n")

        
    
     
        
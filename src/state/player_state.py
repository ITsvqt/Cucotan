from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shared.enums import Resource, DevCard, PlayerColour


class PlayerState:
    

    def __init__ (self, player_id: int,  color: PlayerColour):
        
        self._player_id: int = player_id
        self._color:     PlayerColour = color
        self._name:      str   = f"Pesho {self._player_id}"

        # Board presence (IDs into Board topology)
        self._settlements: set[int] = set()   # vertex_ids with a settlement
        self._cities:      set[int] = set()   # vertex_ids upgraded to city
        self._roads:       set[int] = set()   # edge_ids with a road
        self._cnt_knights_played = 0

        # Hand
        self._resources: dict[Resource, int] = {
            Resource.WOOD:  0,
            Resource.CLAY:  0,
            Resource.SHEEP: 0,
            Resource.GRAIN: 0,
            Resource.ORE :  0
            }
        
        self._dev_cards:  dict[DevCard, int] = {
            DevCard.KNIGHT        : 0,
            DevCard.YEAR_OF_PLENTY: 0,
            DevCard.ROAD_BUILDING : 0,
            DevCard.MONOPOLY      : 0,
            DevCard.VICTORY_POINT : 0
        }

        
        # Unplayable cards this turn, to be added to dev_cards at end of turn
        self._new_dev_cards: list[DevCard] = []
        # Dev card play tracking (reset each turn)
        self._played_dev_card_this_turn: bool = False

        # Accumulated scoring bonuses
        self._victory_points: int    = 0       # sum of: settlements*1 + cities*2 + vp_cards + special_cards
        self._vp_from_dev_cards: int = 0       # hidden until end-game reveal

    # Special card holders (None = nobody has it yet)
    # These live on GameState, 
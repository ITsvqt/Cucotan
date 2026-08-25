from typing import TYPE_CHECKING
from enums import Resource

if TYPE_CHECKING:
    pass

class TradeOffer:
    
    offering_player_id: int
    give:   dict[Resource, int]
    want:   dict[Resource, int]
    # For counter-offers / maritime trades, rules layer handles the variants
    # State just stores "there is an active offer"
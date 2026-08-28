
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enums import DevCard, GamePhase, TurnSubPhase
    from state.player_state import PlayerState
    from state.trade import TradeOffer


class GameState:

    def __init__(self, players: list[PlayerState]):
        
        # Players 
        self._players: list[PlayerState] = [] # index == turn order
        self._current_player_index: int  = 0 

        self._phase: GamePhase = None                  # SETUP_FORWARD | SETUP_BACKWARD | MAIN | ENDED
        # Tracks where we are *within* the current player's turn
        self._turn_sub_phase: TurnSubPhase = None      # PRE_ROLL | POST_ROLL | (setup phases don't use this)

        # Board overlays (IDs only, no object refs)
        self._robber_hex_id: int = None                # which hex the robber is currently on

        # Dice
        self._last_roll: tuple[int, int] = None

        # Decks
        self._dev_card_deck: list[DevCard] = []      # remaining draw pile (ordered; top = index 0)
        # Resource cards are implicit: 95 total minus sum of all player hands
        # (no need to track bank explicitly — rules just check totals)

        # pecial cards
        self._longest_road_owner:  int = None     # player_id
        self._longest_road_length: int = 4         # current longest road length (minimum 5 to award)

        self._largest_army_owner:  int = None    # player_id, or None if unawarded
        self._largest_army_size:   int = 2     # current largest army size (minimum 3 to award)

        # Trade state (transient, cleared after each trade resolves)
        self._pending_trade: TradeOffer | None

        # Setup-phase bookkeeping 
        # During SETUP_FORWARD / SETUP_BACKWARD the player must place settlement THEN road.
        # Track which they've done this setup turn.
        self._setup_placed_settlement: bool
        self._setup_placed_road:       bool

        # Winner 
        self._winner_id: int | None               # set when phase == ENDED
        
        
    @property
    def current_player(self):
        return self._players[self._current_player_index] #! player index might be 1 based, sub -1 to get correct el
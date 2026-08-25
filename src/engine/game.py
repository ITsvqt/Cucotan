from __future__ import annotations
from typing import TYPE_CHECKING

from core.board import Board
from state.game_state import GameState
from state.player_state import PlayerState

from maps.classic_catan_map import ClassicMap
from maps.spread_generation.map_spread_generator import MapSpreadGenerator

if TYPE_CHECKING:
    from enums import PlayerColor

class Game:
    """
    The boundary between the UI and the logic layer.
    Owns the board and state. Exposes one method per player action.
    The UI calls these methods and receives back the new state to render.
    """
    
    def __init__(self, player_colours: list[PlayerColor]):
        
        self._board: Board = self._setup_board()
        self._state: GameState = self._setup_state(player_colours)
        
    @property
    def state(self) -> GameState:
        return self._state
    
    #** Setup ***********************************************************           

    def _setup_board(self) -> Board:
        
        map_ = ClassicMap()
        board = Board(map_)
        MapSpreadGenerator(board).generate
        
        return board
    
    def _setup_state(self, player_colours: list[PlayerColor]) -> GameState:
        players = [ PlayerState(i, c) for i, c in enumerate(player_colours)]
        return GameState(players)
        
        
    

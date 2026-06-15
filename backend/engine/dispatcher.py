# applies actions
from shared.actions import (
    BuildRoad,
    BuildSettlement,
    RollDice,
    EndTurn
)

class Dispatcher:

    def __init__(self, board, state):
        self.board = board
        self.state = state
        
    def dispatch(self, action):

        if isinstance(action, BuildRoad):
            return self._build_road(action)

        if isinstance(action, BuildSettlement):
            return self._build_settlement(action)

        if isinstance(action, RollDice):
            return self._roll_dice(action)

        if isinstance(action, EndTurn):
            return self._end_turn(action)

        raise ValueError("Unknown action")
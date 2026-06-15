# main game loop / orchestrator

from backend.engine.dispatcher import Dispatcher

class Game:

    def __init__(self, board, state):
        self.board = board
        self.state = state
        self.dispatcher = Dispatcher(board, state)
        
    def apply_action(self, action):
        return self.dispatcher.dispatch(action)
    
    def next_turn(self):
        self.state.current_player = (
            (self.state.current_player + 1)
            % len(self.state.players)
        )
        
    def roll_dice(self, player_id: int):
        import random

        dice = (random.randint(1, 6), random.randint(1, 6))
        self.state.dice = dice

        return dice
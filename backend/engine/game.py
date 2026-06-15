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
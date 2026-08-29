from enum import Enum, auto
from enums import PlayerColor
from engine.game import Game

class LobbyStatus(Enum):
    OPEN        = auto(),  # waiting for players
    FULL        = auto(),  # waiting game to start
    IN_PROGRESS = auto()   # game runing



class Lobby():
    
    def __init__(self, lobby_id:int, max_players: int):
        
        self._game: Game = None
        
        self._status = LobbyStatus.OPEN
        self._lobby_id = lobby_id
        
        self._max_players = max_players
        self._available_slots: set  = set(range(max_players))
        
        self._player_token_to_id: dict[str, int] = {} # player_server_uuid : player_state_id
    
    
    @property
    def status(self):
        return self._status
    
    @property
    def game(self):
        return self._game
    
    def start_game(self):
        colors = [PlayerColor.RED, PlayerColor.BLUE, PlayerColor.GREEN, PlayerColor.YELLOW]
        self._game = Game(colors[:self._max_players])
        self._status = LobbyStatus.IN_PROGRESS

        
    def add_player(self, player_token: str) -> bool:
        
        if len(self._available_slots) == 0:
            return False
        
        player_id = min(self._available_slots)
        self._available_slots.remove(player_id)
        
        self._player_token_to_id[player_token] = player_id
        
        if len(self._available_slots) == 0:
            self._status = LobbyStatus.FULL
        
        return True
    
    def remove_player(self, player_token: str):
        assert player_token in self._player_token_to_id
        
        player_id = self._player_token_to_id.pop(player_token)
        self._available_slots.add(player_id)
        
        self._status = LobbyStatus.OPEN
        
    def to_json(self) -> dict:
        return {
            "id": self._lobby_id,
            "players_joined": self._max_players - len(self._available_slots),
            "max_players": self._max_players
        }
        
        
    
        

    
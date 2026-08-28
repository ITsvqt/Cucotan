from enum import Enum, auto

class LobbyStatus(Enum):
    OPEN        = auto(),  # waiting for players
    FULL        = auto(),  # waiting game to start
    IN_PROGRESS = auto()   # game runing



class Lobby():
    
    def __init__(self, max_players: int):
        
        self._status = LobbyStatus.OPEN
        self._available_slots: set  = set(range(max_players))
        self._player_token_to_id: dict[str, int] = {} # player_server_uuid : player_state_id
        
        
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
        

    
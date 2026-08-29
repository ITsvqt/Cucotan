from lobby.Lobby import Lobby, LobbyStatus

import uuid


class LobbyManager():
    
    def __init__(self):
        self._lobbies: dict[int, Lobby] = {}
        self._lobby_counter = 0
        
        self._player_tokens: dict[str, int] = {} # player_uuid: lobby_id
        
        
    def _next_id(self):
        self._lobby_counter += 1
        return self._lobby_counter
    
    def get_lobby(self, lobby_id: int):
        return self._lobbies.get(lobby_id)
    
    def get_open_lobbies_json(self):
        return [
            lobby.to_json()
            for lobby in self._lobbies.values()
            if lobby.status == LobbyStatus.OPEN
        ]

    def start_lobby(self, lobby_id: int) -> bool:
        lobby = self._lobbies.get(lobby_id)
        if lobby is None:
            return False
        lobby.start_game()
        return True
    
    def create_lobby(self, max_players: int) -> tuple[str, int]:
        """ Creates lobby, adds it to the manager, and adds the creator to that lobby. """

        lobby_id = self._next_id()
        new_lobby = Lobby(lobby_id, max_players)
        
        self._lobbies[lobby_id] = new_lobby
        
        player_token = self.add_player_to_lobby(lobby_id)
        
        return (player_token, lobby_id)
    
    def remove_lobby(self, lobby_id: int) -> bool:
        """ Returns True if action succeeded, False otherwise. """
        
        
        if lobby_id not in self._lobbies:
            return False
        
        lobby = self._lobbies[lobby_id]

        for token in lobby._player_token_to_id:
            del self._player_tokens[token]

        del self._lobbies[lobby_id]

        return True
        
    
    def add_player_to_lobby(self, lobby_id: int) -> str:
        """ Returns the generated player token | None if the action failed. """
        
        if lobby_id not in self._lobbies:
            return None # lobby not found
        
        player_token = self._generate_token()
        
        if self._lobbies[lobby_id].add_player(player_token):
            self._player_tokens[player_token] = lobby_id

            return player_token
        
        return None # lobby is full
        
    def remove_player_from_lobby(self, player_token: str) -> bool:
        """ Returns True if action succeeded, False otherwise. """

        if player_token not in self._player_tokens:
            return False
        
        player_lobby_id = self._player_tokens[player_token]

        self._lobbies[player_lobby_id].remove_player(player_token)
        
        del self._player_tokens[player_token]

        return True

        
    def _generate_token(self) -> str:
        """ Generates unique player token. """
        
        while True:
            token = str(uuid.uuid4())
            if token not in self._player_tokens:
                return token
        
        
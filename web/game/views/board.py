from django.shortcuts import render
from django.http import JsonResponse

from engine.game import Game
from enums import PlayerColor

from ..session import lobby_manager

def board_page(request):
    return render(request, 'game/board.html')    
    
def board_data(request, lobby_id):
    lobby = lobby_manager.get_lobby(lobby_id)
    if lobby is None:
        return JsonResponse({"error": "Lobby not found"}, status=404)
    
    game = lobby.game
    if game is None:
        return JsonResponse({"error": "Game not started"}, status=404)
    
    return JsonResponse({"hexes": game.get_hexes_json()})
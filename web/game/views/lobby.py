from django.shortcuts import render
from django.http import JsonResponse

import json

from ..session import lobby_manager


def waiting_room(request, lobby_id):
    return render(request, 'game/lobby.html', {'lobby_id': lobby_id})
    
def start_game(request):
    data = json.loads(request.body)
    lobby_id = data["lobby_id"]

    if lobby_manager.start_lobby(lobby_id) is True:
        return JsonResponse({"status": "ok"})
    else:
        return JsonResponse({"error": "Lobby id is not existant!"}, status = 404)
        

def leave_lobby(request):
    
    data = json.loads(request.body)
    player_token = data["player_token"]
    
    if lobby_manager.remove_player_from_lobby(player_token) is True:
        return JsonResponse({"removed_player_token": player_token})
    else:
        return JsonResponse({"error": "Player token is not in any lobby!"}, status = 404)
    
def remove_lobby(request):
    data = json.loads(request.body)
    lobby_id = data["lobby_id"]
    
    if lobby_manager.remove_lobby(lobby_id) is True:
        return JsonResponse( {"removed_lobby_id": lobby_id})
    else:
        return JsonResponse({"error": "Lobby not found!"}, status = 404)
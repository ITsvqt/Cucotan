from django.shortcuts import render
from django.http import JsonResponse

import json

from ..session import lobby_manager



def home(request):
    return render(request, 'game/home.html')


def get_lobbies(request):
    lobbies = lobby_manager.get_open_lobbies_json()
    return JsonResponse({"lobbies": lobbies})


def create_lobby(request):

    data = json.loads(request.body)
    max_players = data["max_players"]
    
    player_token, lobby_id  = lobby_manager.create_lobby(max_players)

    return JsonResponse( {"new_lobby_id": lobby_id, "player_token": player_token} )


def join_lobby(request):
    
    data = json.loads(request.body)
    lobby_id = data["lobby_id"]
    
    player_token = lobby_manager.add_player_to_lobby(lobby_id)
    
    if player_token is None:
        return JsonResponse({"error": "Lobby not found or full!"}, status = 404)
    else:
        return JsonResponse( {"player_token": player_token})
    

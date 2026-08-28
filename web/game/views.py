from django.shortcuts import render
from django.http import JsonResponse

import json

from lobby.LobbyManager import LobbyManager

# Create your views here.

lobby_manager = LobbyManager()

def home(request):
    return JsonResponse({"message": "Hello, welcome to my Django server!"})
    

def create_lobby(request):

    data = json.loads(request.body)
    max_players = data["max_players"]
    
    player_token, lobby_id  = lobby_manager.create_lobby(max_players)

    return JsonResponse( {"new_lobby_id": lobby_id, "player_token": player_token} )
    
def remove_lobby(request):
    data = json.loads(request.body)
    lobby_id = data["lobby_id"]
    
    if lobby_manager.remove_lobby(lobby_id) is True:
        return JsonResponse( {"removed_lobby_id": lobby_id})
    else:
        return JsonResponse({"error": "Lobby not found!"}, status = 404)


def join_lobby(request):
    data = json.loads(request.body)
    lobby_id = data["lobby_id"]
    
    
    player_token = lobby_manager.add_player_to_lobby(lobby_id)
    
    if player_token is None:
        return JsonResponse({"error": "Lobby not found or full!"}, status = 404)
    else:
        return JsonResponse( {"player_token": player_token})

def leave_lobby(request):
    data = json.loads(request.body)
    player_token = data["player_token"]
    
    if lobby_manager.remove_player_from_lobby(player_token) is True:
        return JsonResponse({"removed_player_token": player_token})
    else:
        return JsonResponse({"error": "Player token is not in any lobby!"}, status = 404)
        

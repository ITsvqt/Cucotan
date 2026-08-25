from django.shortcuts import render
from django.http import JsonResponse

import json

from engine.game import Game
from enums import PlayerColor
# Create your views here.


game_counter = 0

def _get_next_game_counter():
    global game_counter
    game_counter += 1
    return game_counter

active_games = {}

def create_game(request):
    game_id = _get_next_game_counter()

    game = Game([PlayerColor.RED, PlayerColor.BLUE])
    active_games[game_id] = game
    
    return JsonResponse( {"game_id": game_id} )

def join_game(request):
    data = json.loads(request.body)
    game_id = data["game_id"]
    
    if game_id in active_games:
        
        return JsonResponse( {"Success": "GameFound"})
    
    return JsonResponse({"Failure":"GameNotFound"})
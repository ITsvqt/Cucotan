from django.shortcuts import render
from django.http import JsonResponse

import json

from lobby.LobbyManager import LobbyManager

# Create your views here.

lobby_manager = LobbyManager()

def home(request):
    return JsonResponse({"message": "Hello, welcome to my Django server!"})
    
def get_board(request):
    ...


    






        

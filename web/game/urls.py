from django.urls import path

from .views import board, home, lobby


urlpatterns = [
    path(''       , home.home),
    path('create/', home.create_lobby),
    path('join/'  , home.join_lobby),
    path('lobbies/', home.get_lobbies),
    path('leave/', lobby.leave_lobby),
    path('lobby/<int:lobby_id>/', lobby.waiting_room),
    path('start/', lobby.start_game),
    path('board/', board.board_page),
    path('board-data/<int:lobby_id>/', board.board_data)
    # path('remove/', views.remove_lobby)
]
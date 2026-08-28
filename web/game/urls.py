from django.urls import path

from . import views


urlpatterns = [
    path(''       , views.home),
    
    path('create/', views.create_lobby),
    path('join/'  , views.join_lobby),
    path('leave/', views.leave_lobby),
    
    path('remove/', views.remove_lobby)
]
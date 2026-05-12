from django.urls import path
from .views import home, list_games

urlpatterns = [
    path("", home, name="home"),
    path("api/games/", list_games, name="list_games"),
]
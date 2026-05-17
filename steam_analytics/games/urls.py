from django.urls import path

from .views import (
    home,
    list_games
)

urlpatterns = [

    path(
        "",
        home
    ),

    path(
        "api/games/",
        list_games
    ),
]
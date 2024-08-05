from django.urls import path
from . import views

app_name = "math_games"

urlpatterns = [
    path("play/<str:level_name>/", views.play_game, name="play_game"),
    path("success/<str:level_name>/", views.game_success, name="game_success"),
    path("failure/<str:level_name>/", views.game_failure, name="game_failure"),
    path("select_level/", views.select_level, name="select_level"),
]

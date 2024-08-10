from django.urls import path
from . import views

app_name = "sequence_memory"

urlpatterns = [
    path("play/", views.play_game, name="play_game"),
    path("game_over/", views.game_over, name="game_over"),
]

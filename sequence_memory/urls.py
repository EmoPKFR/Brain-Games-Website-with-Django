from django.urls import path
from . import views

app_name = "sequence_memory"

urlpatterns = [
    path('play_game/', views.play_game, name='play_game'),
]
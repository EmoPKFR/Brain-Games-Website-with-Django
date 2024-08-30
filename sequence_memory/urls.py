from django.urls import path
from . import views

app_name = "sequence_memory"

urlpatterns = [
    path('play_game/', views.play_game, name='play_game'),
    path('save_score/', views.save_score, name='save_score'),
]
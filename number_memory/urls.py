from django.urls import path
from . import views

app_name = 'number_memory'

urlpatterns = [
    path('', views.start_game, name='start_game'),
    path('show_number/', views.show_number, name='show_number'),
    path('answer/', views.answer, name='answer'),
    path('check_number/', views.check_number, name='check_number'),
    path('game_over/', views.game_over, name='game_over'),
]
from django.urls import path
from . import views

app_name = "typing_test"

urlpatterns = [
    path('', views.typing_test, name='typing_test'),
    path('calculate/', views.calculate_wpm, name='calculate_wpm'),
]
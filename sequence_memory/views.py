from django.shortcuts import render

def play_game(request):
    return render(request, 'sequence_memory/play_game.html')
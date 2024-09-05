from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import GameScoreSequenceMemory

def play_game(request):
    return render(request, 'sequence_memory/play_game.html',)


@login_required
def save_score(request):
    if request.method == "POST":
        current_score = int(request.POST.get("score", 0))
        profile, created = GameScoreSequenceMemory.objects.get_or_create(user=request.user)
        if current_score > profile.highest_score:
            profile.highest_score = current_score
            profile.save()
        return JsonResponse({"message": "Score saved successfully", "highest_score": profile.highest_score})
    return JsonResponse({"error": "Invalid request"}, status=400)
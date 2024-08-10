from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SequenceMemoryScore
import random

@login_required
def play_game(request):
    score, created = SequenceMemoryScore.objects.get_or_create(user=request.user)

    if request.method == "POST":
        # Get the user's sequence as a list directly
        user_sequence = request.POST.getlist("sequence")
        correct_sequence = request.session.get("sequence", [])

        # Convert both sequences to lists of integers for comparison
        user_sequence = [int(x) for x in user_sequence]
        correct_sequence = [int(x) for x in correct_sequence]

        if user_sequence == correct_sequence:
            score.highest_level += 1
            score.save()
            return redirect("sequence_memory:play_game")
        else:
            return redirect("sequence_memory:game_over")

    # Generate a new sequence for the current level
    sequence = [random.randint(0, 8) for _ in range(score.highest_level + 1)]
    request.session["sequence"] = sequence  # Store as a list of integers

    return render(request, "sequence_memory/play_game.html", {"level": score.highest_level + 1, "sequence": sequence})

@login_required
def game_over(request):
    score = SequenceMemoryScore.objects.get(user=request.user)
    level_reached = score.highest_level
    score.highest_level = 0
    score.save()

    return render(request, "sequence_memory/game_over.html", {"level_reached": level_reached})

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .models import GameScoreNumberMemory
import random

def start_game(request):
    request.session["level"] = 1
    return redirect("number_memory:show_number")

def show_number(request):
    level = request.session.get("level", 1)
    digits = random.randint(10**(level-1), 10**level-1)
    
    # Calculate the time based on the level
    if level <= 3:
        time_to_remember = 3
    else:
        time_to_remember = 3 + (level - 3)

    request.session["number"] = digits

    context = {"number": digits, "level": level, "time_to_remember": time_to_remember}
    return render(request, "number_memory/show_number.html", context)

def answer(request):
    return render(request, "number_memory/answer.html")

def check_number(request):
    if request.method == "POST":
        user_answer = request.POST.get("user_answer")
        correct_answer = str(request.session.get("number"))
        level = request.session.get("level", 1)

        if user_answer == correct_answer:
            request.session["level"] = level + 1
            return redirect("number_memory:show_number")
        else:
            return redirect("number_memory:game_over")
        
    return redirect("number_memory:start_game")

def game_over(request):
    level = request.session.get("level", 1)

    if request.user.is_authenticated:
        # Get the user's highest score from the database
        highest_score_record = GameScoreNumberMemory.objects.filter(user=request.user).order_by('-score').first()

        if highest_score_record:
            # Update the highest score if the current score is higher
            if level > highest_score_record.score:
                highest_score_record.score = level
                highest_score_record.date = timezone.now()
                highest_score_record.save()
        else:
            # If no score exists, create a new record
            highest_score_record = GameScoreNumberMemory.objects.create(user=request.user, score=level, date=timezone.now())

    context = {"level": level, "highest_score": highest_score_record}
    return render(request, "number_memory/game_over.html", context)


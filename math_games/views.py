from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import GameLevel, GameScore
import random

def generate_problem(level):
    if level == "easy":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        operation = random.choice(["+", "-"])
    elif level == "medium":
        a = random.randint(1, 10)
        b = random.randint(1, 10)
        operation = random.choice(["+", "-", "*", "/"])
    elif level == 'hard':
        a = random.randint(10, 30)
        b = random.randint(10, 30)
        operation = random.choice(['+', '-', '*', '/'])
    elif level == 'expert':
        a = random.randint(20, 50)
        b = random.randint(20, 50)
        operation = random.choice(["+", "-", "*", "/"])
    
    problem = f"{a} {operation} {b}"
    answer = eval(problem)
    return problem, answer

@login_required
def play_game(request, level_name):
    level = GameLevel.objects.get(name=level_name)
    if request.method == "POST":
        user_answer = float(request.POST["answer"])
        correct_answer = float(request.session.get('answer'))

        if user_answer == correct_answer:
            score = 10 # For example, 10 points for a correct answer
            GameScore.objects.create(user=request.user, level=level, score=score)
            return redirect("math_games:game_success", level_name=level_name)
        else:
            return redirect("math_games:game_failure", level_name=level_name)
    else:
        problem, answer = generate_problem(level_name)
        request.session['answer'] = answer
        return render(request, "math_games/play_game.html", {"level": level, "problem": problem})

def game_success(request, level_name):
    return render(request, "math_games/game_success.html", {"level_name": level_name})

def game_failure(request, level_name):
    return render(request, "math_games/game_failure.html", {"level_name": level_name})

def select_level(request):
    levels = GameLevel.objects.all()
    return render(request, "math_games/select_level.html", {"levels": levels})


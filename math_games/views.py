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
        operation = "/"
    elif level == 'expert':
        a = random.randint(20, 50)
        b = random.randint(20, 50)
        operation = random.choice(["*", "/"])
    elif level == 'multiplication_by_5':
        a = random.randint(10, 50)
        b = 5
        operation = "*"
    elif level == 'division_by_5':
        a = random.randint(50, 200)
        b = 5
        operation = "/"
    
    problem = f"{a} {operation} {b}"

    #Calculate the answer and handle division separately
    if operation == "/":
        #Ensure we don't divide by zero
        if b == 0:
            b = random.randint(1, 10)  #or any appropriate non-zero value for your level
        answer = round(a / b, 2)  #round to 2 decimal places
    else:
        answer = eval(problem)

    return problem, answer

def play_game(request, level_name):
    level = GameLevel.objects.get(name=level_name)  # Make sure you're using the level object

    # Reset score when switching levels
    if request.session.get("current_level") != level_name:
        request.session["score"] = 0
        request.session["current_level"] = level_name

    if "score" not in request.session:
        request.session["score"] = 0

    if request.method == "POST":
        user_answer_str = request.POST.get("answer", "")

        try:
            # Attempt to convert the user answer to a float
            user_answer = round(float(user_answer_str), 2)
            correct_answer = round(float(request.session.get('answer')), 2)

            if user_answer == correct_answer:
                request.session["score"] += 1
                # Generate a new problem if the answer is correct
                problem, answer = generate_problem(level_name)
                request.session['answer'] = answer
            else:
                # Only save the score if the user is authenticated
                if request.user.is_authenticated:
                    save_score(request, level)  # Pass the level object instead of level_name
                return redirect("math_games:game_failure", level_name=level_name)

        except ValueError:
            # Handle non-numeric input with an error message
            error_message = "Please enter a valid number."
            problem = request.session.get('problem')
            if not problem:
                # Generate a problem if not already present in the session
                problem, answer = generate_problem(level_name)
                request.session['answer'] = answer
            else:
                # Use the existing problem if available
                answer = request.session.get('answer')

            return render(request, "math_games/play_game.html", {
                "level": level,
                "problem": problem,
                "score": request.session["score"],
                "error_message": error_message
            })

    # Generate problem and answer if GET request or if there's no problem in the session
    problem, answer = generate_problem(level_name)
    request.session['problem'] = problem
    request.session['answer'] = answer

    return render(request, "math_games/play_game.html", {"level": level, "problem": problem, "score": request.session["score"]})

@login_required
def reset_game(request, level_name):
    request.session["score"] = 0
    problem, answer = generate_problem(level_name)
    request.session['answer'] = answer
    level = GameLevel.objects.get(name=level_name)
    return render(request, "math_games/play_game.html", {"level": level, "problem": problem, "score": request.session["score"]})

def game_success(request, level_name):
    save_score(request, level_name)
    return render(request, "math_games/game_success.html", {"level_name": level_name})

def game_failure(request, level_name):
    level = GameLevel.objects.get(name=level_name)  # Get the level object
    score = request.session.get("score", 0)
    
    highest_score = None  # Default if not authenticated
    
    if request.user.is_authenticated:
        save_score(request, level)

        # Retrieve the user's highest score for the current level
        game_score = GameScore.objects.filter(user=request.user, level=level).first()
        if game_score:
            highest_score = game_score.highest_score

    request.session["score"] = 0
    
    return render(request, "math_games/game_failure.html", {
        "level_name": level_name,
        "score": score,
        "highest_score": highest_score
    })

def select_level(request):
    levels = GameLevel.objects.all()
    return render(request, "math_games/select_level.html", {"levels": levels})

def save_score(request, level):
    if request.user.is_authenticated:
        score = request.session.get("score", 0)
        user = request.user

        game_score, created = GameScore.objects.get_or_create(user=user, level=level)

        # Update the highest_score if the current score is higher
        if score > game_score.highest_score:
            game_score.highest_score = score
        
        game_score.save()

@login_required
def leaderboard(request):
    # Retrieve the top 10 scores for each level
    levels = {}
    for level in GameLevel.objects.all():
        top_scores = GameScore.objects.filter(level=level).order_by('-highest_score')[:10]
        levels[level.name] = top_scores

    return render(request, "math_games/leaderboard.html", {"levels": levels})
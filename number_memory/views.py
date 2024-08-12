from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.timezone import now
import random

def start_game(request):
    request.session["level"] = 1
    return redirect("number_memory:show_number")

def show_number(request):
    level = request.session.get("level", 1)
    digits = random.randint(10**(level-1), 10**level-1)

    request.session["number"] = digits

    context = {"number": digits, "level": level}
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
    context = {"level": level}
    return render(request, "number_memory/game_over.html", context)


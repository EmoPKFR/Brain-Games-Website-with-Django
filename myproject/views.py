# from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from math_games.models import GameScore as MathGameScore
from sequence_memory.models import GameScoreSequenceMemory
from number_memory.models import GameScoreNumberMemory
from typing_test.models import TypingTestResult

def homepage(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def all_leaderboards(request):
    # Query top 10 scores for each game
    math_game_easy_scores = MathGameScore.objects.filter(level__name='easy').order_by('-highest_score')[:10]
    math_game_medium_scores = MathGameScore.objects.filter(level__name='medium').order_by('-highest_score')[:10]
    math_game_hard_scores = MathGameScore.objects.filter(level__name='hard').order_by('-highest_score')[:10]
    math_game_expert_scores = MathGameScore.objects.filter(level__name='expert').order_by('-highest_score')[:10]
    math_game_multiplication_by_5_scores = MathGameScore.objects.filter(level__name='multiplication_by_5').order_by('-highest_score')[:10]
    math_game_division_by_5_scores = MathGameScore.objects.filter(level__name='division_by_5').order_by('-highest_score')[:10]

    sequence_memory_scores = GameScoreSequenceMemory.objects.order_by('-highest_score')[:10]
    number_memory_scores = GameScoreNumberMemory.objects.order_by('-score')[:10]
    typing_test_scores = TypingTestResult.objects.order_by('-wpm')[:10]

    context = {
        'math_game_easy_scores': math_game_easy_scores,
        'math_game_medium_scores': math_game_medium_scores,
        'math_game_hard_scores': math_game_hard_scores,
        'math_game_expert_scores': math_game_expert_scores,
        'math_game_multiplication_by_5_scores': math_game_multiplication_by_5_scores,
        'math_game_division_by_5_scores': math_game_division_by_5_scores,
        'sequence_memory_scores': sequence_memory_scores,
        'number_memory_scores': number_memory_scores,
        'typing_test_scores': typing_test_scores,
    }

    return render(request, 'all_leaderboards.html', context)
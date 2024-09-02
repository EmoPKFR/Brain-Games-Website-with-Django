from django.shortcuts import render
import random
import time
import json
from django.http import JsonResponse
from typing_test.models import TypingTestResult

SENTENCES = [
    "The gentle breeze rustled the leaves in the quiet forest.",
    "A curious cat explored the hidden corners of the old attic.",
    "Brightly colored balloons floated high above the bustling parade.",
    "The distant mountains were shrouded in a mysterious morning fog.",
    "A chef expertly chopped vegetables for a delicious homemade stew.",
    "Children laughed and played joyfully in the summer sunshine.",
    "A single raindrop fell onto the windowpane, creating a tiny splash.",
    "The intricate pattern on the quilt told a story of ancient times.",
    "Bookshelves filled with novels lined the walls of the cozy library.",
    "The vintage typewriter clicked rhythmically as the author composed their novel.",
    # Add more sentences here
]

def typing_test(request):
    if request.method == 'GET':
        sentence = random.choice(SENTENCES)
        return render(request, 'typing_test/typing_test.html', {'sentence': sentence})

def calculate_wpm(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sentence = data.get('sentence').strip()
            typed_text = data.get('typed_text').strip()
            time_taken = float(data.get('time_taken'))

            print(f"Sentence: {sentence}")
            print(f"Typed Text: {typed_text}")
            print(f"Time Taken: {time_taken} seconds")

            # Split both sentence and typed text into words
            sentence_words = sentence.split()
            typed_words = typed_text.split()

            # Calculate word-level accuracy
            correct_words = sum(1 for i, word in enumerate(typed_words) if i < len(sentence_words) and word == sentence_words[i])
            accuracy = (correct_words / len(sentence_words)) * 100 if sentence_words else 0

            # Calculate WPM
            wpm = (len(typed_words) / time_taken) * 60

            print(f"Correct Words: {correct_words}")
            print(f"WPM: {wpm}")
            print(f"Accuracy: {accuracy}")

            if request.user.is_authenticated:
                TypingTestResult.objects.create(
                    user=request.user,
                    wpm=wpm,
                    accuracy=accuracy
                )

            return JsonResponse({'wpm': wpm, 'accuracy': accuracy})

        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
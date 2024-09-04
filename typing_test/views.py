from django.shortcuts import render
import random
import time
import json
from django.http import JsonResponse
from typing_test.models import TypingTestResult

SENTENCES = [
    "The garden is filled with vibrant flowers. Butterflies dance among the petals. Bees buzz from bloom to bloom. A fountain trickles softly in the center. The grass is lush and green. Birds chirp in the nearby trees. A wooden bench sits beneath a willow tree. The air is fragrant with the scent of roses.",
    
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

            # Split both sentence and typed text into words
            sentence_words = sentence.split()
            typed_words = typed_text.split()

            # Calculate word-level accuracy based on typed words
            correct_words = sum(1 for i, word in enumerate(typed_words) if i < len(sentence_words) and word == sentence_words[i])
            accuracy = (correct_words / len(typed_words)) * 100 if typed_words else 0  # Accuracy based on typed words only

            # Calculate WPM (Words per Minute) and round to nearest integer
            wpm = round((len(typed_words) / time_taken) * 60)

            print(f"Correct Words: {correct_words}")
            print(f"WPM: {wpm}")
            print(f"Accuracy: {accuracy}")

            # Save the result if the user is authenticated
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



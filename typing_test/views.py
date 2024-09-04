from django.shortcuts import render
import random
import json
from django.http import JsonResponse
from typing_test.models import TypingTestResult

SENTENCES = [
    """The garden is filled with vibrant flowers.
        Butterflies dance among the petals.
        Bees buzz from bloom to bloom.
        A fountain trickles softly in the center.
        The grass is lush and green.
        Birds chirp in the nearby trees.
        A wooden bench sits beneath a willow tree.
        The air is fragrant with the scent of roses.""",
    """The alarm rings at 6:00 AM sharp.
        I stretch my arms and yawn widely.
        The coffee machine hums to life.
        I pour a cup of steaming coffee.
        Breakfast is a bowl of oatmeal with fruit.
        I read the news on my phone.
        After breakfast, I brush my teeth.
        I choose an outfit for the day.""",
    """The sky is overcast and gray.
        Raindrops patter against the window.
        The streets are slick with water.
        People hurry by with umbrellas.
        The air is cool and damp.
        Puddles form on the sidewalks.
        Cars splash through the rain.
        The trees sway gently in the wind.""",
    """I chop onions and garlic for the sauce.
        The pasta boils in a large pot.
        The smell of sautéing vegetables fills the kitchen.
        I stir the tomato sauce slowly.
        Fresh herbs are added to the mixture.
        The table is set with plates and cutlery.
        A loaf of bread is warmed in the oven.
        The pasta is drained and added to the sauce.""",
    """The park is peaceful and quiet.
        Children play on the swings and slides.
        A couple jogs along the path.
        Ducks swim lazily in the pond.
        The sun filters through the leaves of tall trees.
        A soft breeze rustles the branches.
        People sit on benches, reading or chatting.
        A man walks his dog on a leash."""
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
                # Check if there's an existing high score for the user
                existing_result = TypingTestResult.objects.filter(user=request.user).order_by('-wpm').first()
                
                if existing_result is None or wpm > existing_result.wpm:
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

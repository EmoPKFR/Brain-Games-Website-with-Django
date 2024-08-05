from django.db import models
from django.contrib.auth.models import User

class GameLevel(models.Model):
    LEVEL_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
        ("expert", "Expert"),
    ]
    name = models.CharField(max_length=6, choices=LEVEL_CHOICES, unique=True)

    def __str__(self):
        return self.name
    

class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(GameLevel, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
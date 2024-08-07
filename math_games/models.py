from django.db import models
from django.contrib.auth.models import User

class GameLevel(models.Model):
    LEVEL_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
        ("expert", "Expert"),
        ("multiplication_by_5", "Multiplication by 5"),
        ("division_by_5", "Division by 5"),
    ]
    name = models.CharField(max_length=20, choices=LEVEL_CHOICES, unique=True)

    def __str__(self):
        return self.name
    

class GameScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey(GameLevel, on_delete=models.CASCADE)
    highest_score = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'level')

    def __str__(self):
        return f"{self.user.username} - {self.level.name} - Highest Score: {self.highest_score}"
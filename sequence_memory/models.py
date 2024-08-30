from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class GameScoreSequenceMemory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    highest_score = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - Highest Score: {self.highest_score}"

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class GameScoreNumberMemory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"User: {self.user.username} - Score: {self.score}"

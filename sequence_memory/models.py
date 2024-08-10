from django.db import models
from django.contrib.auth.models import User

class SequenceMemoryScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    highest_level = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Level {self.highest_level}"

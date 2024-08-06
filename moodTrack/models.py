from django.db import models
from authentication.models import User


# Create your models here.
class MoodTrack(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.CharField(max_length=30)
    mood = models.CharField(max_length=30)
    context = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.mood} - {self.timestamp}"

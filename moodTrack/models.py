from django.db import models
from authentication.models import User


# Create your models here.
class MoodTrack(models.Model):

    CONTEXT_CHOICES = [
        ("wakeup", "Upon Waking"),
        ("before_study", "Before Study"),
        ("after_study", "After Study"),
        ("end_day", "End of Day"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateField(auto_now_add=True)
    mood = models.CharField(max_length=30)
    context = models.CharField(max_length=20, choices=CONTEXT_CHOICES, blank=True, null=True)
    custom_context = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.mood} - {self.timestamp}"

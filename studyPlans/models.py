from django.db import models
from authentication.models import User

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    details = models.CharField(max_length=50, blank=True)
    deadlines = models.DateField(null=True, blank=True)
    complexityLevel = [("low", "Low"), ("normal", "Normal"), ("high", "High")]
    complexity = models.CharField(max_length=20, choices=complexityLevel)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.deadlines} - {self.details}- {self.complexity}"

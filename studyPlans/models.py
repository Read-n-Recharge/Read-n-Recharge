from django.db import models
from authentication.models import User

# Create your models here.


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False)
    details = models.CharField(max_length=50, blank=True)
    deadlines = models.DateField(null=True, blank=True)
    complexityLevel = [("low", "Low"), ("normal", "Normal"), ("high", "High")]
    complexity = models.CharField(max_length=20, choices=complexityLevel, blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"


class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    studyMethod = models.CharField(max_length=50, null=False)
    stress_level = models.CharField(max_length=10, null=True)
    noise_level = models.CharField(max_length=10, null=True)
    environment = models.CharField(max_length=10, null=True)
    session_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task}"

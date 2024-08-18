from django.db import models
from authentication.models import User

# Create your models here.


class UserPoint(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.total_points}"

    def add_points(self, points):
        self.total_points += points
        self.save() 

    def deduct_points(self, points):
        if self.total_points >= points:
            self.total_points -= points
            self.save()
        else:
            raise ValueError("Not enough points")


class PointRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.points} points - {self.action}"

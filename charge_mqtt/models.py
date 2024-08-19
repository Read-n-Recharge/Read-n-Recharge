from django.db import models
from authentication.models import User

class RelayActivation(models.Model):
    relay_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.IntegerField()

    def __str__(self):
        return f"Relay {self.relay_id} activated by {self.user} for {self.duration} seconds"

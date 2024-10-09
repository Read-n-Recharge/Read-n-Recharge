from django.db import models
from authentication.models import User

class RelayActivation(models.Model):
    relay_id = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    duration = models.IntegerField()
    password = models.CharField(max_length=6)

    def __str__(self):
        return f"Relay {self.relay_id} activated by {self.user} for {self.duration} seconds"

class RelayUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    relay_id = models.IntegerField()
    usage_current = models.FloatField()
    carbon_credit = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Usage for Charging {self.relay_id} usage current {self.usage_current} receive carbon credit {self.carbon_credit}."
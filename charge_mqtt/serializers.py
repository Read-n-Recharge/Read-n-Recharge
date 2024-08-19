from rest_framework import serializers
from .models import RelayActivation

class RelayStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelayActivation
        fields = ['relay_id', 'user','duration','start_time']
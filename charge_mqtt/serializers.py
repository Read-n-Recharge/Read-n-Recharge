from rest_framework import serializers
from .models import RelayActivation, RelayUsage

class RelayStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelayActivation
        fields = ['relay_id', 'user','duration','start_time']

class RelayusageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelayUsage
        fields = ['user', 'relay_id', 'usage_current', 'carbon_credit', 'created_at']
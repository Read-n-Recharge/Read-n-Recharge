from rest_framework import serializers
from .models import RelayStatus

class RelayStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelayStatus
        fields = ['relay1_status', 'relay2_status']
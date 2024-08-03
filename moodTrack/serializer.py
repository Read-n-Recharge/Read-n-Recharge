from .models import MoodTrack
from rest_framework import serializers


class MoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodTrack
        fields = "__all__"

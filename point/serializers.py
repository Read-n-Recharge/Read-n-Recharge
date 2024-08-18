from rest_framework import serializers
from .models import UserPoint, PointRecord


class UserPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPoint
        fields = ["total_points"]


class PointRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointRecord
        fields = ["points", "action", "timestamp"]

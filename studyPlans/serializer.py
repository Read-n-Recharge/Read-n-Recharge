from .models import Task
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            "id",
            "user",
            "title",
            "deadlines",
            "details",
            "complexity",
            "complete",
        )
        read_only_fields = ["user"]

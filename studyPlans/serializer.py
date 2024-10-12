from .models import Task, StudySession
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

class StudySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudySession
        fields = ['task', 'studyMethod', 'stress_level', 'noise_level', 'session_date']

from rest_framework import viewsets
from .serializer import MoodSerializer
from .models import MoodTrack
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class MoodViewSet(viewsets.ModelViewSet):
    queryset = MoodTrack.objects.all()
    serializer_class = MoodSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

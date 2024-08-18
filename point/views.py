from rest_framework import viewsets
from .models import UserPoint, PointRecord
from .serializers import UserPointSerializer, PointRecordSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class UserPointViewSet(viewsets.ModelViewSet):
    queryset = UserPoint.objects.all()
    serializer_class = UserPointSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PointRecordViewSet(viewsets.ModelViewSet):
    queryset = PointRecord.objects.all()
    serializer_class = PointRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        point_record = serializer.save(user=self.request.user)
        user_point, created = UserPoint.objects.get_or_create(user=self.request.user)
        if point_record.action == "add":
            user_point.add_points(point_record.points)
        elif point_record.action == "use":
            user_point.deduct_points(point_record.points)
        else:
            raise ValueError("Invalid action specified")

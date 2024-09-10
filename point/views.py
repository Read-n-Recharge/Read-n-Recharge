from rest_framework import viewsets
from .models import UserPoint, PointRecord
from .serializers import UserPointSerializer, PointRecordSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


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

        if point_record.action not in ["add", "use"]:
            raise serializers.ValidationError(
                {"action": "Invalid action specified. Must be 'add' or 'use'."}
            )

        if point_record.points < 0:
            raise serializers.ValidationError(
                {"points": "Points must be a positive number."}
            )

        if point_record.action == "add":
            user_point.add_points(point_record.points)
        elif point_record.action == "use":
            if user_point.total_points < point_record.points:
                raise serializers.ValidationError(
                    {
                        "points": f"Points not enough to use. Current total points: {user_point.total_points}"
                    }
                )
            user_point.deduct_points(point_record.points)
        else:
            raise ValueError("Invalid action specified")


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_point_history(request):

    user = request.user
    point_history = PointRecord.objects.filter(user=user).order_by("-timestamp")[:7]
    serializer = PointRecordSerializer(point_history, many=True)

    return Response(serializer.data)

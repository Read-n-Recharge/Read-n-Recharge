from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserPointViewSet, PointRecordViewSet, get_point_history

router = DefaultRouter()
router.register(r"total_points", UserPointViewSet, basename="total_points")
router.register(r"points_record", PointRecordViewSet, basename="points_record")

urlpatterns = [
    path("", include(router.urls)),
    path("point_history/", get_point_history, name="point_history"),
]

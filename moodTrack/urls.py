# urls.py
from django.urls import path
from .views import MoodViewSet

mood_list = MoodViewSet.as_view({"get": "list", "post": "create"})
mood_detail = MoodViewSet.as_view(
    {"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}
)

urlpatterns = [
    path("", mood_list, name="mood-list"),
    path("<int:pk>/", mood_detail, name="mood-detail"),
]

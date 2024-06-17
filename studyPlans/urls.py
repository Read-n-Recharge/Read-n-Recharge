from django.urls import path
from .views import UserTaskView, CreateTaskView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path("tasks/create", CreateTaskView.as_view(), name="create-tasks"),
    path("tasks/update/<int:pk>", TaskUpdateView.as_view(), name="update-tasks"),
    path("tasks/delete/<int:pk>", TaskDeleteView.as_view(), name="delete-tasks"),
    path("tasks", UserTaskView.as_view(), name="list-tasks"),
]

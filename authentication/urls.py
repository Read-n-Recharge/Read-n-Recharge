from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path
from . import views

urlpatterns = [
  path("token/",views.MyTokenObtainPairView.as_view()),
  path("token/refresh/",TokenRefreshView.as_view()),
  path("register/",views.RegisterView.as_view()),
  path("dashboard/",views.dashboard),
  path('form/<int:user_id>/', views.StudyPreferenceView.as_view()),
  path("user/<int:pk>/", views.UserDetailView.as_view()), 
]
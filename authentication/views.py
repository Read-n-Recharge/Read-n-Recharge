# Create your views here.
from .models import User, StudyPrefernce
from .serializer import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    StudyPreferenceSerializer,
    UserSerializer,
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.exceptions import NotFound


User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user_id = response.data.get("id")
        return Response({"user_id": user_id}, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.method == "GET":
        response = f"Hey {request.user}, you are seeing a get request"
        return Response({"response": response}, status=status.HTTP_200_OK)
    elif request.method == "POST":
        text = request.POST.get("text")
        response = f"Hi {request.user} , your text is {text}"
        return Response({"response": response}, status=status.HTTP_200_OK)

    return Response({}, status=status.HTTP_400_BAD_REQUEST)


class StudyPreferenceView(generics.CreateAPIView):
    queryset = StudyPrefernce.objects.all()
    permission_classes = [AllowAny]
    serializer_class = StudyPreferenceSerializer

    def perform_create(self, serializer):
        user_id = self.kwargs.get("user_id")
        try:
            user = User.objects.get(pk=user_id)
            return serializer.save(user=user)
        except User.DoesNotExist:
            raise NotFound({"error": "User not found."})


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class UserStudyPreferenceView(generics.RetrieveAPIView):
    serializer_class = StudyPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            user = User.objects.get(pk=user_id)
            return StudyPrefernce.objects.get(user=user)
        except User.DoesNotExist:
            raise NotFound({"error": "User not found."})
        except StudyPrefernce.DoesNotExist:
            raise NotFound({"error": "Study preference not found for this user."})

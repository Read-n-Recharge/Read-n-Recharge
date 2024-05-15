from django.shortcuts import render

# Create your views here.
from .models import User,Profile
from .serializer import UserSerializer,MyTokenObtainPairSerializer,RegisterSerializer
from rest_framework.decorators import api_view ,permission_classes  #convert Django views into RESTful API views.
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics,status #generic views from DRF,provide commonly used patterns for creating API views.
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

class MyTokenObtainPairView(TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
  queryset= User.objects.all()
  permission_classes = ([AllowAny])
  serializer_class = RegisterSerializer

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])

def dashboard(request):
  if request.method == 'GET':
    response = f'Hey {request.user}, you are seeing a get request'
    return Response({'response':response},status=status.HTTP_200_OK)
  elif request.method == 'POST':
    text = request.POST.get("text")
    response = f"Hi {request.user} , your text is {text}"
    return Response({'response':response},status=status.HTTP_200_OK)
  
  return Response({},status=status.HTTP_400_BAD_REQUEST)
  



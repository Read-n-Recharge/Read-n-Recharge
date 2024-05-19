from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ChargeStationINFO, TempData
from .serializers import ChargeStationSerializers, TempDataSerializers


# Create your views here.
# class ChargeStationAPIView (APIView):
#     def post(self, request, format=None):
#         serializer = ChargeStationSerializers(data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TempDataAPIView (APIView):
    def post(self, request, format=None):
        serializer = TempDataSerializers(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

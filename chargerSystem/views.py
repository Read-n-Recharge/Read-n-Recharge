from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import RelayStatus
from .serializers import RelayStatusSerializer



def control_relay_view(request):
    return render(request, 'test_control_relay.html')

class RelayCommandView(APIView):
    parser_classes = [JSONParser]

    def get(self, request, *args, **kwargs):
        relay_status = RelayStatus.objects.last()
        if relay_status:
            serialzer = RelayStatusSerializer(relay_status)
            return Response(serialzer.data)
        else:
            return Response({"relay1": "STOP", "relay2": "STOP"})
        
    def post(self, request, *arge, **kwarge):
        relay = request.data.get('relay')
        command  = request.data.get('command')

        if relay == 'relay1':
            RelayStatus.objects.update_or_create(id=1, defaults={'relay1_status': command})
        elif relay == 'relay2':
            RelayStatus.objects.update_or_create(id=1, defaults={'relay2_status': command})

        return Response({'status': 'success'})   


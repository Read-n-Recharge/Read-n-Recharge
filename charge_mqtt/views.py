import json
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status

from charge_mqtt.mqtt_helpers import connect_mqtt
from .relay_manager import control_relay, stop_relay, check_relay_status, validate_relay_id
from .models import RelayActivation, RelayUsage
from .utils import send_password_email, validate_password
from .relay_manager import stop_relay as stop_relay_in_manager
from .serializers import RelayusageSerializer


@csrf_exempt
def start_mqtt_listener(request):
    if request.method == "POST":
        client = connect_mqtt()
        if client:
            return JsonResponse({"status": "listening"})
        else:
            return JsonResponse(
                {"status": "failed", "reason": "Connection issue"}, status=500
            )
    return JsonResponse(
        {"status": "failed", "reason": "invalid request method"}, status=400
    )

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_relay(request, relayID):
    user = request.user
    data = json.loads(request.body)
    duration = data.get("duration", 15)
    password = data.get("password")

    # Validate relayID and password
    validation_response = validate_relay_id(relayID)
    if validation_response:
        return validation_response

    if not validate_password(password):
        return JsonResponse(
            {"status": "failed", "reason": "Password must be a 6-digit number."}, status=400
        )

    # Log the relay activation
    activation = RelayActivation.objects.create(
        relay_id=relayID, user=user, duration=duration * 60, password=password
    )

    # Send password email
    send_password_email(user, relayID, password)

    # Control relay
    return control_relay(relayID, duration * 60, user.id, password)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def stop_relay(request, relayID):
    user = request.user
    validation_response = validate_relay_id(relayID)
    if validation_response:
        return validation_response

    return stop_relay_in_manager(relayID, user.id)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def relay_usage(request):
    user = request.user
    relay_usage_data = RelayUsage.objects.filter(user=user)

    if relay_usage_data.exists():
        serializer = RelayusageSerializer(relay_usage_data, many=True)
        return JsonResponse(serializer.data, safe=False ,status = status.HTTP_200_OK)
    else:
        return JsonResponse({"error": "No relay usage data found for this user."}, status=status.HTTP_404_NOT_FOUND)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def relay_status_view(request):
    """View to check the status of all relays."""
    return JsonResponse(check_relay_status())

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from charge_mqtt.mqtt_helpers import connect_mqtt
from .relay_manager import control_relay, stop_relay, check_relay_status
from .models import RelayActivation

# Constants for default duration
DEFAULT_DURATION_MINUTES = 15


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_relay(request, relayID):
    """API to start the relay for a given duration (in minutes)."""
    if request.method == "POST":
        data = json.loads(request.body)
        duration = (
            data.get("duration", DEFAULT_DURATION_MINUTES) * 60
        )  # Convert to seconds

        # Log the relay activation
        RelayActivation.objects.create(
            relay_id=relayID, user=request.user, duration=duration
        )

        return control_relay(relayID, duration)
    return JsonResponse(
        {"status": "failed", "reason": "Invalid request method"}, status=400
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def stop_relay(request, relayID):
    """API to stop a specific relay."""
    if request.method == "POST":
        return stop_relay(relayID)
    return JsonResponse(
        {"status": "failed", "reason": "Invalid request method"}, status=400
    )


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
        {"status": "failed", "reason": "Invalid request method"}, status=400
    )


@csrf_exempt
@api_view(["GET"])
def relay_status_view(request):
    """API to return the current status of all relays."""
    return check_relay_status(request)


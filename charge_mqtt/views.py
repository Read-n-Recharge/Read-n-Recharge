import json
import threading
import paho.mqtt.client as mqtt
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from charge_mqtt.mqtt_helpers import connect_mqtt
from .serializers import RelayActivation
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import RelayActivation
from .relay_manager import relay_status





def check_emqx_connection():
    client = connect_mqtt()
    if client:
        topic = "emqx/esp32"
        message = "Django server started successfully"
        client.publish(topic, message)
        print(f"Message sent to {topic}: {message}")
    else:
        print("Failed to send message due to connection issue")


def validate_relay_id(relayID):
    """Helper to validate if the relay ID exists."""
    if relayID not in relay_status:
        return JsonResponse(
            {"status": "failed", "reason": f"Relay {relayID} does not exist"},
            status=400,
        )
    return None


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


def control_relay_module(relayID, duration):
    client = connect_mqtt()
    validation_response = validate_relay_id(relayID)
    if validation_response:
        return validation_response

    if client:
        if relay_status.get(relayID) == "active":
            return JsonResponse(
                {"status": "failed", "reason": f"Relay {relayID} is already active"},
                status=400,
            )

        topic = f"relay/{relayID}/control"
        # Send the START command with the duration included in the message payload
        payload = json.dumps({"command": "START", "duration": duration})
        client.publish(topic, payload)
        print(f"Sent command '{payload}' to '{topic}' for {duration} seconds")

        relay_status[relayID] = {"status": "active", "duration": duration}

        def stop_relay():
            client.publish(topic, json.dumps({"command": "STOP"}))
            print(f"Sent command 'STOP' to '{topic}' after {duration} seconds")
            client.disconnect()

            # Update relay status to inactive
            relay_status[relayID] = {"status": "inactive", "duration": 0}

        timer = threading.Timer(duration, stop_relay)
        timer.start()

        return JsonResponse(
            {"status": "success", "relay": relayID, "duration": duration}
        )
    else:
        return JsonResponse(
            {"status": "failed", "reason": "Failed to Connect to MQTT Broker"},
            status=500,
        )


def stop_relay_module(relayID):
    client = connect_mqtt()
    validation_response = validate_relay_id(relayID)
    if validation_response:
        return validation_response

    if client:
        if relay_status.get(relayID) == "inactive":
            return JsonResponse(
                {"status": "failed", "reason": f"Relay {relayID} is already inactive"},
                status=400,
            )

        topic = f"relay/{relayID}/control"
        client.publish(topic, json.dumps({"command": "STOP"}))
        print(f"Sent command 'STOP' to '{topic}'")
        client.disconnect()

        # Update relay status to inactive
        relay_status[relayID] = "inactive"

        return JsonResponse(
            {"status": "success", "relay": relayID, "action": "stopped"}
        )
    else:
        return JsonResponse(
            {"status": "failed", "reason": "Failed to Connect to MQTT Broker"},
            status=500,
        )


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_relay(request, relayID):
    user = request.user

    validation_response = validate_relay_id(relayID)
    if validation_response:
        return validation_response

    if request.method == "POST":
        data = json.loads(request.body)
        duration = data.get("duration", 15)

        # Log the relay activation
        activation = RelayActivation.objects.create(
            relay_id=relayID,
            user=user,
            duration=duration * 60,
        )

        # Control the relay module
        return control_relay_module(relayID, duration * 60)

    return JsonResponse(
        {"status": "failed", "reason": "Invalid request method"}, status=400
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def stop_relay(request, relayID):
    user = request.user
    validation_response = validate_relay_id(relayID)
    if validation_response:
        return validation_response

    if request.method == "POST":
        return stop_relay_module(relayID)

    return JsonResponse(
        {"status": "failed", "reason": "Invalid request method"}, status=400
    )


@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_relay(request, relayID):
    user = request.user
    validation_response = validate_relay_id(relayID)
    if validation_response:
        return validation_response

    if request.method == "POST":
        data = json.loads(request.body)
        duration = data.get("duration", 15)

        activation = RelayActivation.objects.create(
            relay_id=relayID,
            user=user,
            duration=duration * 60,
        )

        return control_relay_module(relayID, duration * 60)

    return JsonResponse(
        {"status": "failed", "reason": "Invalid request method"}, status=400
    )


# Function to check the status of all relays
def check_relay_status(request):
    return JsonResponse(relay_status)

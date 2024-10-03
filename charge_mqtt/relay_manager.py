import threading
from django.http import JsonResponse
from .mqtt_helpers import connect_mqtt, publish_message

DEFAULT_RELAY_STATUS = "inactive"
RELAY_STATUS_ACTIVE = "active"
RELAY_DURATION_MULTIPLIER = 60  # Convert minutes to seconds


relay_status = {
    1: {"status": DEFAULT_RELAY_STATUS, "duration": 0},
    2: {"status": DEFAULT_RELAY_STATUS, "duration": 0},
    3: {"status": DEFAULT_RELAY_STATUS, "duration": 0},
}


def control_relay(relayID, duration, user_id):
    """Control the relay to start for the specified duration and stop automatically."""
    client = connect_mqtt()
    if not client:
        return JsonResponse(
            {"status": "failed", "reason": "Failed to Connect to MQTT Broker"},
            status=500,
        )

    if relay_status[relayID]["status"] == RELAY_STATUS_ACTIVE:
        return JsonResponse(
            {"status": "failed", "reason": f"Relay {relayID} is already active"},
            status=400,
        )

    # Activate the relay for the specified duration
    publish_message(
        client, f"{relayID}/control", {"command": "START", "duration": duration, "user_id": user_id}
    )
    relay_status[relayID] = {"status": RELAY_STATUS_ACTIVE, "duration": duration}

    def stop_relay():
        publish_message(client, f"{relayID}/control", {"command": "STOP", "user_id": user_id})
        relay_status[relayID] = {"status": DEFAULT_RELAY_STATUS, "duration": 0}
        client.disconnect()

    # Stop the relay after the duration
    timer = threading.Timer(duration, stop_relay)
    timer.start()

    return JsonResponse({"status": "success", "relay": relayID, "duration": duration, "user_id": user_id})


def stop_relay(relayID, user_id):
    """Stop the relay."""
    client = connect_mqtt()
    if not client:
        return JsonResponse(
            {"status": "failed", "reason": "Failed to Connect to MQTT Broker"},
            status=500,
        )

    if relay_status[relayID]["status"] == DEFAULT_RELAY_STATUS:
        return JsonResponse(
            {"status": "failed", "reason": f"Relay {relayID} is already inactive"},
            status=400,
        )

    publish_message(client, f"{relayID}/control", {"command": "STOP", "user_id": user_id})
    relay_status[relayID] = {"status": DEFAULT_RELAY_STATUS, "duration": 0}
    client.disconnect()

    return JsonResponse({"status": "success", "relay": relayID, "action": "stopped", "user_id": user_id})


def check_relay_status(request):
    """Check the status of all relays, including their status and remaining duration."""
    return JsonResponse(relay_status)

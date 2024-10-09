import threading, json
import paho.mqtt.client as mqtt
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


def validate_relay_id(relayID):
    """"Helper to validate if the relay ID exists."""
    if relayID not in relay_status:
        return JsonResponse(
            {"status": "failed", "reason": f"Relay {relayID} does not exits."},
            status= 400,
        )
    return None

def control_relay(relayID, duration, user_id, password):
    """Control the relay to start for the specified duration and stop automatically."""
    client = connect_mqtt()
    validate_response = validate_relay_id(relayID)
    if validate_response:
        return validate_response

    if client:
        if relay_status[relayID]["status"] == RELAY_STATUS_ACTIVE:
            return JsonResponse(
                {"status": "failed", "reason": f"Relay {relayID} is already active"},
                status=400,
            )
        
        topic = f"relay/{relayID}/control"
        payload = json.dumps({"command": "START", "duration": duration, "user_id": user_id, "password": password})
        client.publish(topic, payload)
        relay_status[relayID] = {"status": RELAY_STATUS_ACTIVE, "duration": duration}
    
        # def stop_relay():
        #     client.publish(topic, json.dumps({"command": "STOP", "user_id": user_id}))
        #     relay_status[relayID] = {"status": DEFAULT_RELAY_STATUS, "duration": 0}
        #     client.disconnect()

        # timer = threading.Timer(duration, stop_relay)
        # timer.start()

        return JsonResponse(
            {"status": "success", "relay": relayID, "duration": duration, "user_id": user_id}
        )
    else:
        return JsonResponse(
            {"status": "failed", "reason": "Failed to Connect to MQTT Broker"},
            status=500,
        )


def stop_relay(relayID, user_id):
    """Stop the relay."""
    client = connect_mqtt()
    validate_response = validate_relay_id(relayID)
    if validate_response:
        return validate_response

    if relay_status[relayID]["status"] == RELAY_STATUS_ACTIVE:
       try:
            topic = f"relay/{relayID}/control"
            payload = json.dumps({"command": "STOP", "user_id": user_id})
            client.publish(topic, payload)
            print(f"Published STOP command for relay {relayID}")

            relay_status[relayID] = {"status": DEFAULT_RELAY_STATUS, "duration": 0}

            client.disconnect()
            return JsonResponse({
                "status": "success", 
                "relay": relayID, 
                "action": "stopped", 
                "user_id": user_id
            })
       except Exception as e:
            print(f"Error while stopping relay {relayID}: {e}")
            return JsonResponse({
                "status": "failed", 
                "reason": f"Error while stopping relay {relayID}: {e}"
            }, status=500)
    else:
        # หาก relay อยู่ในสถานะ inactive แล้ว ให้แจ้งว่าไม่สามารถหยุดได้
        return JsonResponse({
            "status": "failed", 
            "reason": f"Relay {relayID} is already inactive"
        }, status=400)

def update_relay_status(relayID, status):
    """Update relay status based on MQTT message."""
    if relayID in relay_status:
        relay_status[relayID] = {"status": status}
        print(f"Relay {relayID} status updated to {status}")
    else:
        print(f"Relay {relayID} not found.")

def check_relay_status(request):
    """Check the status of all relays."""
    return JsonResponse(relay_status)

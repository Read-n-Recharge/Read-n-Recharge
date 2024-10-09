import os
import json
import paho.mqtt.client as mqtt
from django.conf import settings

# MQTT connection credentials and settings (constants)
MQTT_BROKER_HOST = "wb35b1b7.ala.asia-southeast1.emqxsl.com"
MQTT_BROKER_PORT = 8883
MQTT_USERNAME = "PutipongSailen"
MQTT_PASSWORD = "Putipong.48852"
MQTT_TOPIC_PREFIX = "relay/"
MQTT_KEEP_ALIVE = 60  # Seconds
CA_CERT_PATH = os.path.join(os.path.dirname(__file__), "cert/emqxsl-ca.crt")


def on_message(client, userdata, message):
    """Callback when a message is received."""
    payload = message.payload.decode("utf-8")
    data = json.loads(payload)

    if message.topic == "relay/status":
        relay_id = data.get("relayID")
        status = data.get("status")
        
        # Update the relay status based on the incoming message
        from .relay_manager import update_relay_status
        update_relay_status(relay_id, status)

    print(f"Received message '{payload}' on topic '{message.topic}' with QoS {message.qos}")


def connect_mqtt():
    """Connect to the MQTT broker with TLS and authentication."""
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.tls_set(ca_certs=CA_CERT_PATH)

    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, MQTT_KEEP_ALIVE)
        client.on_message = on_message

        client.subscribe("relay/status")

        client.loop_start()
        print("Connected to MQTT Broker")
        return client
    except Exception as e:
        print(f"Failed to connect to MQTT Broker: {e}")
        return None


def publish_message(client, topic_suffix, payload):
    """Helper to publish MQTT message."""
    topic = f"relay/{topic_suffix}"
    payload_str = json.dumps(payload)
    client.publish(topic, payload_str)
    print(f"Published {payload_str} to {topic}")
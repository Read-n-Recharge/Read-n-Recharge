import os
import json
import paho.mqtt.client as mqtt

from authentication.models import User
from charge_mqtt.models import RelayUsage

# MQTT connection credentials and settings (constants)
MQTT_BROKER_HOST = "wb35b1b7.ala.asia-southeast1.emqxsl.com"
MQTT_BROKER_PORT = 8883
MQTT_USERNAME = "PutipongSailen"
MQTT_PASSWORD = "Putipong.48852"
MQTT_TOPIC_PREFIX = "relay/"
MQTT_KEEP_ALIVE = 60  # Seconds
CA_CERT_PATH = os.path.join(os.path.dirname(__file__), "cert/emqxsl-ca.crt")


def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    data = json.loads(payload)

    user_id = data.get("user_id")
    relay_id = data.get("relayID")
    duration = data.get("duration")
    usage_current = data.get("usage_current")
    carbon_credit = data.get("carbon_credit")

    user = User.objects.get(id=user_id)

    RelayUsage.object.create(
        user=user,
        relay_id=relay_id,
        duration=duration,
        usage_current=usage_current,
        carbon_credit=carbon_credit,
    )

    print(f"Data from SUB topic: relay: {relay_id} carbon credit: {carbon_credit}.")


def connect_mqtt():
    """Connect to the MQTT broker with TLS and authentication."""
    client = mqtt.Client()

    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.tls_set(ca_certs=CA_CERT_PATH)

    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, MQTT_KEEP_ALIVE)
        print("Connected to MQTT Broker")
    except Exception as e:
        print(f"Failed to connect to MQTT Broker: {e}")
        return None

    client.on_message = on_message

    client.subscribe ("save/database")
    client.loop_start()
    return client


def publish_message(client, topic_suffix, payload):
    """Helper to publish MQTT message."""
    topic = f"{MQTT_TOPIC_PREFIX}{topic_suffix}"
    payload_str = json.dumps(payload)
    client.publish(topic, payload_str)
    print(f"Published {payload_str} to {topic}")

from django.apps import AppConfig
from .mqtt_helpers import connect_mqtt

# Constants for MQTT message and topic
MQTT_STARTUP_TOPIC = "emqx/esp32"
MQTT_STARTUP_MESSAGE = "Django server started successfully"

class ChargeMqttConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'charge_mqtt'

    def ready(self):
        client = connect_mqtt()
        if client:
            client.publish(MQTT_STARTUP_TOPIC, MQTT_STARTUP_MESSAGE)
            print("MQTT connection and message sent on startup.")

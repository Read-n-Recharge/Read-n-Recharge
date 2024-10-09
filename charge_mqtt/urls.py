from django.urls import path
from .views import check_relay_status, start_mqtt_listener, start_relay, stop_relay, relay_usage

urlpatterns = [
    path("start-listening/", start_mqtt_listener, name="start_mqtt_listener"),
    path("relay/<int:relayID>/start/", start_relay, name="start_relay"),
    path("relay/status/", check_relay_status, name="check_relay_status"),
    path("relay/<int:relayID>/stop/", stop_relay, name="stop_relay"),
    path("relay-usage/", relay_usage, name="relay_usage"),
]

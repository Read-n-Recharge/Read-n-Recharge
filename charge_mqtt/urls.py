from django.urls import path
from .views import start_mqtt_listener, start_relay

urlpatterns = [
    path('start-listening/', start_mqtt_listener, name='start_mqtt_listener'),
    path('relay/<int:relayID>/start/', start_relay, name='start_relay'),
]
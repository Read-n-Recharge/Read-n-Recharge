from django.urls import path
from .views import start_mqtt_listener, start_relay, stop_relay

urlpatterns = [
    path('start-listening/', start_mqtt_listener, name='start_mqtt_listener'),
    path('relay/<int:module_number>/start/', start_relay, name='start_relay'),
    path('relay/<int:module_number>/stop/', stop_relay, name='stop_relay')
]
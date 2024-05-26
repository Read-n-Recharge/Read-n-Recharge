from django.urls import path 
from .views import RelayCommandView, control_relay_view


urlpatterns = [
    path('api/relay-command/', RelayCommandView.as_view(), name = 'relay-command'),
    path('control-relay/', control_relay_view, name = 'control-relay')
]
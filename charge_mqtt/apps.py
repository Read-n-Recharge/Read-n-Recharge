from django.apps import AppConfig


class ChargeMqttConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'charge_mqtt'

    def ready(self):
        from .views import check_emqx_connection
        check_emqx_connection()
        self.has_run = True
    
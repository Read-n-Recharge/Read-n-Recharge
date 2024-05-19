from rest_framework import serializers
from .models import ChargeStationINFO, TempData

# class ChargeStationSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = ChargeStationINFO
#         field = ['VoltageDetect', 'BatteryStatus', 'VoltageUsingPerDay']

class TempDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = TempData
        field = ['temp', 'humidity']
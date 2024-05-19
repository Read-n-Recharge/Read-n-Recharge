from django.db import models

# Create your models here.

# class ChargeStationINFO(models.Model):
#     Voltage_detect = models.FloatField(max_length=100)
#     Battery_status = models.CharField(max_length=100)
#     Voltage_using_perDay = models.FloatField(max_length= 100)
#     TimeStamp = models = models.DateTimeField(auto_now_add=True)

class TempData(models.Model):
    temp = models.FloatField(max_length= 100)
    humidity = models.FloatField(max_length= 100)
    TimeStamp = models = models.DateTimeField(auto_now_add=True)



    


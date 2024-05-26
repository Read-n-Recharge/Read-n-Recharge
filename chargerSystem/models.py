from django.db import models

# Create your models here.
class RelayStatus(models.Model) :
    relay1_status = models.CharField(max_length=10, choices=[('START', 'Start'), ('STOP', 'Stop')])
    relay2_status = models.CharField(max_length=10, choices=[('START', 'Start'), ('STOP', 'Stop')])



    


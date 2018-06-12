from django.db import models

# Create your models here.
class activeMembers(models.Model):
    mac_adress = models.CharField(max_length=100)
    ping_date = models.DateTimeField('ping date')

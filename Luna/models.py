from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class HydroponicSystem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Maybe in real world app it would be better to use some kind of time series database like influxdb
# as it looks like some sensor data but it was specified to use postgresql
# but influx does not have django ORM support
class Reading(models.Model):
    hydroponic_system = models.ForeignKey(
        HydroponicSystem, on_delete=models.CASCADE, related_name="readings"
    )
    temperature = models.FloatField()
    ph = models.FloatField()
    tds = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hydroponic_system.name} - {self.timestamp}"

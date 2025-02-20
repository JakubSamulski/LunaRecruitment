from django.db import models


# Create your models here.
class HydroponicSystem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Reading(models.Model):
    hydroponic_system = models.ForeignKey(HydroponicSystem, on_delete=models.CASCADE)
    temperature = models.FloatField()
    ph = models.FloatField()
    tds = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hydroponic_system.name} - {self.timestamp}"

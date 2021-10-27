from django.db import models

class Settings(models.Model):
    selectedMode = models.CharField(max_length=20)
    refreshInterval = models.PositiveIntegerField(default=1000)

class WateringSchedule(models.Model):
    time = models.TimeField()

class Modes(models.Model):
    mode = models.CharField(max_length=20)
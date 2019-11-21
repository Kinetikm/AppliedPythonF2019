from django.db import models, backends
import datetime
import time
from django.contrib.auth import get_user_model


class Airport(models.Model):
    airport_name = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.airport_name


class Aircraft(models.Model):
    aircraft_type = models.CharField(max_length=100, primary_key=True)

    def __str__(self):
        return self.aircraft_type


class AirFlight(models.Model):
    departure_time = models.DateTimeField("departure time", db_index=True)
    arrival_time = models.DateTimeField("arrival time", db_index=True)
    travel_time = models.PositiveIntegerField("travel time", db_index=True, default=0)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE)
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)

    class Meta:
        ordering = ('departure_time',)
        verbose_name_plural = 'Airflights'

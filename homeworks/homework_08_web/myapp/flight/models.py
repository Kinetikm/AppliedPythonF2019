from django.db import models
import datetime
import time


class Airport(models.Model):
    id = models.AutoField(primary_key=True)
    airport_name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'airport'


class Aircraft(models.Model):
    id = models.AutoField(primary_key=True)
    aircraft_type = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = 'aircraft'


class AirFlight(models.Model):
    id = models.AutoField(primary_key=True, blank=True)
    departure_time = models.DateTimeField("departure time", db_index=True)
    arrival_time = models.DateTimeField("arrival time", db_index=True)
    travel_time = models.PositiveIntegerField("travel time", db_index=True, default=0)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, to_field='airport_name')
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, to_field='aircraft_type')

    class Meta:
        db_table = 'airflight'
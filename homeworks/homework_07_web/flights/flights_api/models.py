from django.db import models


class AircraftType(models.Model):
    aircaft_type = models.CharField(max_length=20, primary_key=True)


class Airports(models.Model):
    airport = models.CharField(max_length=10, primary_key=True)


class Flights(models.Model):
    flight_id = models.AutoField(primary_key=True)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    flight_time = models.PositiveIntegerField()
    destination_airport = models.ForeignKey(Airports, on_delete=models.CASCADE, to_field='airport')
    aircraft_type = models.ForeignKey(AircraftType, on_delete=models.CASCADE, to_field='aircaft_type')


class RequestLog(models.Model):
    request_method = models.CharField(max_length=10)
    request_body = models.CharField(max_length=255)
    request_path = models.CharField(max_length=255)
    request_time = models.FloatField()

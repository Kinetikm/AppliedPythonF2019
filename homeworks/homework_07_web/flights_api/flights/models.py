from django.db import models


class Aircraft(models.Model):
    aircraft_model = models.CharField(max_length=255, verbose_name='Aircraft', primary_key=True)

    def __str__(self):
        return self.aircraft_model


class Destination(models.Model):
    airport = models.CharField(max_length=255, verbose_name='Destination', primary_key=True)

    def __str__(self):
        return self.airport


class Flight(models.Model):
    departure = models.DateTimeField(verbose_name='Departure_time')
    arrival = models.DateTimeField(verbose_name='Arrival_time')
    travel = models.CharField(max_length=255, verbose_name='Travel_time_in_hours')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, to_field='airport')
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, to_field='aircraft_model')

    def save(self, *args, **kwargs):
        if not self.travel:
            self.travel = self.arrival - self.departure
        super(Flight, self).save(*args, **kwargs)

    def __str__(self):
        return 'Flight ' + self.flight_id


class RequestLog(models.Model):
    request_method = models.CharField(max_length=20)
    server_hostname = models.CharField(max_length=255)
    request_path = models.CharField(max_length=255)
    request_body = models.CharField(max_length=255)
    response_status = models.IntegerField()
    response_body = models.CharField(max_length=255)
    run_time = models.FloatField()

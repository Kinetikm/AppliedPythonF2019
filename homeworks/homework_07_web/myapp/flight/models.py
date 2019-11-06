from django.db import models


class Airport(models.Model):
    airport_name = models.CharField(verbose_name="airport name", max_length=100, primary_key=True)

    # class Meta:
    #     db_table = 'airport'

    def __str__(self):
        return self.airport_name


class Aircraft(models.Model):
    aircraft_type = models.CharField(verbose_name="airport name", max_length=100, primary_key=True)

    # class Meta:
    #     db_table = 'aircraft'
    def __str__(self):
        return self.aircraft_type


class AirFlight(models.Model):
    departure_time = models.DateTimeField("departure time", db_index=True)
    arrival_time = models.DateTimeField("arrival time", db_index=True)
    travel_time = models.PositiveIntegerField("travel time", db_index=True)
    airport = models.ForeignKey(Airport, on_delete=models.CASCADE, to_field='airport_name')
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, to_field='aircraft_type')

    # class Meta:
    #     db_table = 'airflight'

    def save(self, *args, **kwargs):
        if not self.travel:
            self.travel = str(self.arrival_time - self.departure_time)
        super(AirFlight, self).save(*args, **kwargs)

    def __str__(self):
        return 'Flight ' + str(self.id)

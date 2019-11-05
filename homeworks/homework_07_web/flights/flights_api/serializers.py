from rest_framework import serializers
from .models import Flights, AircraftType

class AircraftSerializer(serializers.ModelSerializer):
    class Meta:
        model = AircraftType
        fields = '__all__'
class FlightSerializer(serializers.ModelSerializer):
#    flight_id = serializers.IntegerField()
#    arrival_time = serializers.DateTimeField()
#    departure_time = serializers.DateTimeField()
#    flight_time = serializers.IntegerField(min_value=0)
#    destination_airport = serializers.CharField()
#    aircraft_type = AircraftSerializer()
    class Meta:
        model = Flights
        fields = '__all__'


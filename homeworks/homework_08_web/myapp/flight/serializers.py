from rest_framework import serializers
from .models import Aircraft, Airport, AirFlight


class AircraftFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Aircraft
        fields = 'aircraft_type'


class AirportFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Airport
        fields = 'airport_name'


class AirFlightFieldsSerializer(serializers.ModelSerializer):
    airport = serializers.PrimaryKeyRelatedField(read_only=True)
    aircraft = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AirFlight
        fields = ('departure_time', 'arrival_time', 'airport', 'aircraft')


class AirFlightAllSerializer(serializers.ModelSerializer):
    airport = serializers.PrimaryKeyRelatedField(read_only=True)
    aircraft = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AirFlight
        fields = '__all__'

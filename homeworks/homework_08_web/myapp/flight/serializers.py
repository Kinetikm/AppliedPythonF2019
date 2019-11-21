from rest_framework import serializers
from .models import AirFlight, Aircraft, Airport
from django.core.exceptions import ObjectDoesNotExist


class AirportSerializer(serializers.ModelSerializer):
    airport = serializers.CharField(max_length=100)

    class Meta:
        model = Airport
        fields = ('airport_name')


class AircraftSerializer(serializers.ModelSerializer):
    aircraft = serializers.CharField(max_length=100)

    class Meta:
        model = Aircraft
        fields = ('aircraft_type')


class AirFlightFieldsSerializer(serializers.ModelSerializer):
    departure_time = serializers.DateTimeField()
    arrival_time = serializers.DateTimeField()
    airport = serializers.CharField(max_length=100)
    aircraft = serializers.CharField(max_length=100)

    class Meta:
        model = AirFlight
        fields = ('departure_time', 'arrival_time', 'airport', 'aircraft')

    def create(self, validated_data):
        airports_data = validated_data.pop('airport')
        airport = Airport.objects.create(**{"airport_name": airports_data})
        aircraft_data = validated_data.pop('aircraft')
        aircraft = Aircraft.objects.create(**{"aircraft_type": aircraft_data})
        departure_time = validated_data.pop('departure_time')
        arrival_time = validated_data.pop('arrival_time')
        flight = AirFlight.objects.create(
            **{"departure_time": departure_time, "arrival_time": arrival_time, "airport": airport,
               "aircraft": aircraft})
        return flight

    def update(self, instance, validated_data):
        airports_data = validated_data.pop('airport')
        try:
            airport = Airport.objects.get(pk=airports_data)
        except ObjectDoesNotExist:
            airport = Airport.objects.create(**{"airport_name": airports_data})

        aircraft_data = validated_data.pop('aircraft')
        try:
            aircraft = Aircraft.objects.get(pk=aircraft_data)
        except ObjectDoesNotExist:
            aircraft = Aircraft.objects.create(**{"aircraft_type": aircraft_data})

        instance.departure_time = validated_data.get('departure_time', instance.departure_time)
        instance.arrival_time = validated_data.get('arrival_time', instance.arrival_time)
        instance.airport = validated_data.get('airport', airport)
        instance.aircraft = validated_data.get('aircraft', aircraft)
        instance.save()
        return instance


class AirFlightAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirFlight
        fields = '__all__'

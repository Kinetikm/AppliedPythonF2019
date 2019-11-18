from rest_framework import serializers
from .models import AirFlight, Aircraft, Airport

class AirportSerializer(serializers.ModelSerializer):
    airflight1 = serializers.HyperlinkedIdentityField('airflight1')
    class Meta:
        model = Airport
        fields = ('airport_name')

class AircraftSerializer(serializers.ModelSerializer):
    airflight2 = serializers.HyperlinkedIdentityField('airflight2')
    class Meta:
        model = Aircraft
        fields = ('aircraft_type')

class AirFlightFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirFlight
        fields = ('departure_time', 'arrival_time', 'airport', 'aircraft')

    def create(self, validated_data):
        return AirFlight.objects.create(**validated_data)

class AirFlightAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirFlight
        fields = '__all__'

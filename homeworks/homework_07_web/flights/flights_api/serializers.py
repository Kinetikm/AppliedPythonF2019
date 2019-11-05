from rest_framework import serializers
from .models import Flights, AircraftType


class AircraftSerializer(serializers.ModelSerializer):

    class Meta:
        model = AircraftType
        fields = '__all__'


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flights
        fields = '__all__'

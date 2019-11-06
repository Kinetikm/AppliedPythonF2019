from rest_framework import serializers
from .models import Aircraft, Airport, AirFlight



class AirFlightFieldsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirFlight
        fields = ('departure_time', 'arrival_time', 'airport', 'aircraft')


class AirFlightAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = AirFlight
        fields = '__all__'



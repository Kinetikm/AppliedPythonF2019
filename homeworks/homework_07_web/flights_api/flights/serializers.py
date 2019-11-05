from rest_framework import serializers
from flights.models import Flight


class FlightsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = ('departure', 'arrival', 'destination', 'aircraft')


class FlightsAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = '__all__'

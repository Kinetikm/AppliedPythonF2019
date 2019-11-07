from rest_framework import serializers
from flights.models import Flight, RequestLog


class FlightsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = ('departure', 'arrival', 'destination', 'aircraft')


class FlightsAllSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = '__all__'


class LogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestLog
        fields = '__all__'

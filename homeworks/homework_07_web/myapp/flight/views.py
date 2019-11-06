from rest_framework import generics
from .serializers import *


class FlightListAPIView(generics.ListAPIView):
    serializer_class = AirFlightAllSerializer
    queryset = AirFlight.objects.all()


class FlightListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = AirFlightFieldsSerializer
    queryset = AirFlight.objects.all()


class FlightDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AirFlightFieldsSerializer
    queryset = AirFlight.objects.all()


class FlightDepListView(generics.ListAPIView):
    serializer_class = AirFlightAllSerializer
    queryset = AirFlight.objects.all().order_by('departure_time')


class FlightArrListView(generics.ListAPIView):
    serializer_class = AirFlightAllSerializer
    queryset = AirFlight.objects.all().order_by('arrival_time')

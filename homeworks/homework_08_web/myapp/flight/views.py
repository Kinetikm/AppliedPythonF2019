from rest_framework import generics
from .serializers import *


class FlightListAPIView(generics.ListAPIView):
    queryset = AirFlight.objects.all()
    serializer_class = AirFlightAllSerializer



class FlightListCreateAPIView(generics.ListCreateAPIView):
    queryset = AirFlight.objects.all()
    serializer_class = AirFlightFieldsSerializer



class FlightDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AirFlight.objects.all()
    serializer_class = AirFlightFieldsSerializer



class FlightDepListView(generics.ListAPIView):
    queryset = AirFlight.objects.all().order_by('departure_time')
    serializer_class = AirFlightAllSerializer



class FlightArrListView(generics.ListAPIView):
    queryset = AirFlight.objects.all().order_by('arrival_time')
    serializer_class = AirFlightAllSerializer


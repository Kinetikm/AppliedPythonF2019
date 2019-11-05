from rest_framework import generics
from flights.serializers import *
from flights.models import Flight, Aircraft, Destination


class FlightsListView(generics.ListAPIView):
    serializer_class = FlightsAllSerializer
    queryset = Flight.objects.all()


class FlightsListCreateView(generics.ListCreateAPIView):
    serializer_class = FlightsListSerializer
    queryset = Flight.objects.all()


class FlightDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FlightsListSerializer
    queryset = Flight.objects.all()


class FlightsDepListView(generics.ListAPIView):
    serializer_class = FlightsAllSerializer
    queryset = Flight.objects.all().order_by('departure')


class FlightsArrListView(generics.ListAPIView):
    serializer_class = FlightsAllSerializer
    queryset = Flight.objects.all().order_by('arrival')

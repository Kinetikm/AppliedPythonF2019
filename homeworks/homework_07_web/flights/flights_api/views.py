from rest_framework import generics, mixins

from .models import Flights, Airports, AircraftType
from .serializers import FlightSerializer


class FlightListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = FlightSerializer
    queryset = Flights.objects.all()


class FlightDetailAPIView(
        generics.RetrieveUpdateDestroyAPIView,
        mixins.UpdateModelMixin):

    serializer_class = FlightSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def get_queryset(self):
        flight_id = self.kwargs.get('pk')
        return Flights.objects.filter(flight_id=flight_id)

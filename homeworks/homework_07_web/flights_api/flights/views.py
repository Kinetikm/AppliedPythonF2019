from rest_framework import generics
from flights.serializers import *
from flights.models import Flight, RequestLog
from .rq_log.mixins import RequestLogViewMixin


class FlightsListView(RequestLogViewMixin, generics.ListAPIView):
    serializer_class = FlightsAllSerializer
    queryset = Flight.objects.all()


class FlightsListCreateView(RequestLogViewMixin, generics.ListCreateAPIView):
    serializer_class = FlightsListSerializer
    queryset = Flight.objects.all()


class FlightDetailView(RequestLogViewMixin, generics.RetrieveUpdateDestroyAPIView):
    serializer_class = FlightsListSerializer
    queryset = Flight.objects.all()


class FlightsDepListView(RequestLogViewMixin, generics.ListAPIView):
    serializer_class = FlightsAllSerializer
    queryset = Flight.objects.all().order_by('departure')


class FlightsArrListView(RequestLogViewMixin, generics.ListAPIView):
    serializer_class = FlightsAllSerializer
    queryset = Flight.objects.all().order_by('arrival')


class LogsListView(generics.ListAPIView):
    serializer_class = LogListSerializer
    queryset = RequestLog.objects.all()

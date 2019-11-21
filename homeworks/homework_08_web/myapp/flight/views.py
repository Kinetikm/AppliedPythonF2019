from rest_framework.generics import get_object_or_404
from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from rest_framework import status


@api_view(["POST"])
def create_flight(request):
    serializer = AirFlightFieldsSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def flight_details(request, pk):
    flight = AirFlight.objects.get(id=pk)
    serializer = AirFlightAllSerializer(flight)
    return Response(serializer.data)

@api_view(["GET", "PUT"])
def flight_update(request, pk):
    flight = AirFlight.objects.get(id=pk)
    if request.method == "PUT":
        serializer = AirFlightFieldsSerializer(flight, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response({"error": serializer.errors})
    serializer = AirFlightAllSerializer(flight)
    return Response(serializer.data)

@api_view(["GET"])
def flights_list(request):
    fligths = AirFlight.objects.all()
    serializer = AirFlightAllSerializer(fligths, many=True)
    return Response({"flights": serializer.data})


def delete_user(request, pk):
    user = get_object_or_404(AirFlight, id=pk)
    user.delete()
    return Response({"message": "Deleted"})


class FlightCreateView(generics.CreateAPIView):
    serializer_class = AirFlightFieldsSerializer


class FlightDetailView(generics.RetrieveAPIView):
    queryset = AirFlight.objects.all()
    serializer_class = AirFlightAllSerializer

class FlightUpdateView(generics.RetrieveUpdateAPIView):
    queryset = AirFlight.objects.all()
    serializer_class = AirFlightFieldsSerializer

class FlightsListView(generics.ListAPIView):
    queryset = AirFlight.objects.all()
    serializer_class = AirFlightAllSerializer


class FlightDeleteView(generics.RetrieveDestroyAPIView):
    queryset = AirFlight.objects.all()

    def get(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
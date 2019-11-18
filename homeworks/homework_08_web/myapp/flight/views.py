from rest_framework import generics, permissions
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response



class AirFlightView(APIView):
    def get(self, request):
        fligths = AirFlight.objects.all()
        # the many param informs the serializer that it will be serializing more than a single article.
        serializer = AirFlightAllSerializer(fligths, many=True)
        print(1)
        return Response({"flights": serializer.data})

    def post(self, request):
        serializer = AirFlightFieldsSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"success": "Article '{}' created successfully"})



# class FlightListAPIView(generics.ListAPIView):
#     queryset = AirFlight.objects.all()
#     serializer_class = AirFlightAllSerializer
#
#
#
# class FlightListCreateAPIView(generics.ListCreateAPIView):
#     queryset = AirFlight.objects.all()
#     serializer_class = AirFlightFieldsSerializer
#
#
#
# class FlightDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = AirFlight.objects.all()
#     serializer_class = AirFlightFieldsSerializer
#
#
#
# class FlightDepListView(generics.ListAPIView):
#     queryset = AirFlight.objects.all().order_by('departure_time')
#     serializer_class = AirFlightAllSerializer
#
#
#
# class FlightArrListView(generics.ListAPIView):
#     queryset = AirFlight.objects.all().order_by('arrival_time')
#     serializer_class = AirFlightAllSerializer
#

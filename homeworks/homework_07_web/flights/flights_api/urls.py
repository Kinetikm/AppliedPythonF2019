from django.urls import path

from .views import FlightListCreateAPIView, FlightDetailAPIView

app_name = "flights_api"

urlpatterns = [
    path('flights/', FlightListCreateAPIView.as_view()),
    path('flights/<int:pk>', FlightDetailAPIView.as_view()),
]

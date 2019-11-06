from django.conf.urls import url
from .views import FlightDetailAPIView, FlightListAPIView, FlightListCreateAPIView, FlightDepListView, FlightArrListView

urlpatterns = [
    url('all', FlightListAPIView.as_view()),
    url('create', FlightListCreateAPIView.as_view()),
    url('<int:pk>', FlightDetailAPIView.as_view()),
    url('dep_sort', FlightDepListView.as_view()),
    url('air_sort', FlightArrListView.as_view()),
]

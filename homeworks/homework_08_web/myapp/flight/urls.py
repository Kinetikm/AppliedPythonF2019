from django.conf.urls import url
from .views import FlightDetailAPIView, FlightListAPIView, FlightListCreateAPIView, FlightDepListView, FlightArrListView

urlpatterns = [
    url(r'all', FlightListAPIView.as_view()),
    url(r'create/', FlightListCreateAPIView.as_view()),
    url(r'<int:pk>', FlightDetailAPIView.as_view()),
    url(r'dep_sort', FlightDepListView.as_view()),
    url(r'air_sort', FlightArrListView.as_view()),
]
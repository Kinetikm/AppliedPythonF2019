from django.conf.urls import url
from .views import FlightCreateView, FlightDetailView, FlightsListView, FlightUpdateView, FlightDeleteView

urlpatterns = [
    url(r'^flight/create/$', FlightCreateView.as_view(), name="flight_create"),
    url(r'^flights/list/$', FlightsListView.as_view(), name="flights_list"),
    url(r'^flights/(?P<pk>\d+)/detail/$', FlightDetailView.as_view(), name="flight_detail"),
    url(r'^flights/(?P<pk>\d+)/update/$', FlightUpdateView.as_view(), name="flight_update"),
    url(r'^flights/(?P<pk>\d+)/delete/$', FlightDeleteView.as_view(), name="flight_delete"),
]

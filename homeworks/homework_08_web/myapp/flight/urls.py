from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^flight/create/$', views.create_flight, name="flight_create"),
    url(r'^flights/list/$', views.flights_list, name="flights_list"),
    url(r'^flights/(?P<pk>\d+)/detail/$', views.flight_details, name="flight_detail"),
    url(r'^flights/(?P<pk>\d+)/update/$', views.flight_update, name="flight_update"),
    url(r'^flights/(?P<pk>\d+)/delete/$', views.delete_flight, name="flight_delete"),
]

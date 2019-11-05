from django.urls import path, include
from flights.views import *

app_name = 'flight'
urlpatterns = [
    path('all/', FlightsListView.as_view()),
    path('flight/create/', FlightsListCreateView.as_view()),
    path('flight/<int:pk>/', FlightDetailView.as_view()),
    path('all/dep_sort/', FlightsDepListView.as_view()),
    path('all/air_sort/', FlightsArrListView.as_view()),
]

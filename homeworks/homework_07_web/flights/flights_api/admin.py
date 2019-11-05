from django.contrib import admin

from .models import Flights, Airports, AircraftType

admin.site.register(Airports)
admin.site.register(Flights)
admin.site.register(AircraftType)

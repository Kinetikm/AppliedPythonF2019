from django.contrib import admin

from .models import Flights, Airports, AircraftType, RequestLog

admin.site.register(Airports)
admin.site.register(Flights)
admin.site.register(AircraftType)
admin.site.register(RequestLog)

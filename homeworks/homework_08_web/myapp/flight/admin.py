from django.contrib import admin
from .models import AirFlight, Aircraft, Airport

admin.site.register(AirFlight)
admin.site.register(Airport)
admin.site.register(Aircraft)

from django.contrib import admin
from .models import AirFlight, Airport, Aircraft

admin.site.register(AirFlight)
admin.site.register(Airport)
admin.site.register(Aircraft)

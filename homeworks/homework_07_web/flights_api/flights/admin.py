from django.contrib import admin

from flights.models import Flight, Aircraft, Destination


admin.site.register(Flight)
admin.site.register(Aircraft)
admin.site.register(Destination)

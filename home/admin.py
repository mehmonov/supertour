from django.contrib import admin

from .models import  Destination, TourPackage, Booking


admin.site.register(Destination)
admin.site.register(TourPackage)
admin.site.register(Booking)


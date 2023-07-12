from django.contrib import admin

from offices.models import City, Country, Location

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Location)
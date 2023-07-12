from django.contrib import admin
from .models import Tribe, Squad, Location, Staff, Country, Admin, City
# Register your models here.
admin.site.register(Tribe)
admin.site.register(Squad)
admin.site.register(Staff)
admin.site.register(Country)
admin.site.register(Location)
admin.site.register(Admin)
admin.site.register(City)

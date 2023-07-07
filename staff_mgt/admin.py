from django.contrib import admin
from .models import Tribe, Squad, Location, Staff, Region, Admin
# Register your models here.
admin.site.register(Tribe)
admin.site.register(Squad)
admin.site.register(Staff)
admin.site.register(Region)
admin.site.register(Location)
admin.site.register(Admin)

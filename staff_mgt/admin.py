from django.contrib import admin
from .models import Tribe, Squad, OfficeAddress, Staff, Region, Admin
# Register your models here.
admin.site.register(Tribe)
admin.site.register(Squad)
admin.site.register(Staff)
admin.site.register(Region)
admin.site.register(OfficeAddress)
admin.site.register(Admin)

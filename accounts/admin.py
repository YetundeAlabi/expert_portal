from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from accounts.models import User, ActivityLog

# Register your models here.
class UserAdmin(BaseUserAdmin):

    ordering = ('email',)  # Set the ordering field to 'email'
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')  # Add 'role', 'is_staff', and 'is_active' to the list_display field
    list_filter = ('is_staff', 'is_superuser', 'is_active')  # Add 'role' to the list_filter field
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ("Dates", {"fields": ("last_login",)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
admin.site.register(User, UserAdmin)
admin.site.register(ActivityLog)
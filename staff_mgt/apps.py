from django.apps import AppConfig


class StaffMgtConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "staff_mgt"

    def ready(self):
      import staff_mgt.signals
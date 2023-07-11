
from celery import app


from django.conf import settings
from django.utils import timezone

from staff_mgt.models import Staff
# @app.task()

def suspend_staff():
    #check list of all staffs suspension date
    # if suspend date is today suspend
    today = timezone.now().date()
    staff_to_suspend = Staff.objects.values_list("suspension_date", flat=True
                                    ).filter(suspension_date=today
                                    ).update(is_active= not Staff.is_active, suspension_date='')
    # for staff_id in staff_to_suspend:
    #     instance = Staff.objects.get(id=staff_id)

    # instance.is_active = not instance.is_active
    # instance.save(update_fields=["is_active"])
    return staff_to_suspend
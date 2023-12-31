from django.utils import timezone

from staff_mgt.models import Staff
from expert_portal.celery import app

@app.task()
def suspend_staff():
    #check list of all staffs whose suspension date is today
    # if suspend date is today suspend
    today = timezone.now().date()
    staff_to_suspend = Staff.objects.filter(suspension_date=today
                                            ).update(is_active=False, suspension_date=None)
    
    return "Done suspending staff"
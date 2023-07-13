
from django.db.models import F
from django.utils import timezone

from staff_mgt.models import Staff
from staff_mgt.serializers import StaffSerializer
from expert_portal.celery import app

@app.task()
def suspend_staff():
    #check list of all staffs suspension date
    # if suspend date is today suspend
    today = timezone.now().date()
    print(today)
    
    
    staff_to_suspend = Staff.objects.filter(suspension_date__isnull=False, suspension_date=today
                                            ).update(is_active= ~F("is_active"), suspension_date=None)
    # print(staff_to_suspend.is_active)
    for staff in staff_to_suspend:
        print(staff.is_active)
    staff_to_suspend.update(is_active= ~F("is_active"), suspension_date=None)
    # for staff in staff_to_suspend:
    #     print(staff.is_active)
    # updated_staff_to_suspend = Staff.objects.filter(id__in=staff_to_suspend.values_list("id", flat=True))
    # serialized_data = StaffSerializer(updated_staff_to_suspend, many=True).data
    # for staff in staff_to_suspend:
    #     print(staff.is_active)
    # print(staff_to_suspend.is_active)
    

    # for staff_id in staff_to_suspend:
    #     instance = Staff.objects.get(id=staff_id)

    # instance.is_active = not instance.is_active
    # instance.save(update_fields=["is_active"])
    return serialized_data
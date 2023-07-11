import smtplib
import csv
import pandas as pd
from celery import shared_task

from django.http import HttpResponse

from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone

from staff_mgt.models import Staff

@shared_task
def send_email(data):
    try:
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            from_email=settings.EMAIL_HOST_USER,
            to=[data['to_email']]
        )
        email.send()
    except smtplib.SMTPException as e:
        print(f"An error occured: {e}")



def export_data(serializer, file_name):

    response = HttpResponse(content_type='text/csv')
    response["Content-Disposition"] = f'attachment; filename={file_name} '

    writer = csv.writer(response)
    writer.writerow(serializer.child.fields.keys())

    for obj in serializer.data:
        writer.writerow(obj.values())

    return response

@shared_task
def suspend_staff(instance):
    #check list of all staffs suspension date
    # if suspend date is today suspend
    today = timezone.now().date()
    staff_to_suspend = Staff.objects.values_list("suspension_date", flat=True).filter(suspension_date=today
                                                                ).update(is_active= not is_active, suspension_date='')
    for staff_id in staff_to_suspend:
        instance = Staff.objects.get(id=staff_id)

    instance.is_active = not instance.is_active
    instance.save(update_fields=["is_active"])
    return instance
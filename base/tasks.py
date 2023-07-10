import smtplib
import csv
import pandas as pd
from celery import shared_task

from django.http import HttpResponse

from django.core.mail import EmailMessage
from django.conf import settings


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



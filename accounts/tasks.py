import smtplib
import csv
import pandas as pd
from celery import app

from django.http import HttpResponse

from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone

from staff_mgt.models import Staff

# @app.task()
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

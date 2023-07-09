import smtplib
import csv
import pandas as pd
from celery import shared_task

from django.http import HttpResponse

from django.core.mail import EmailMessage
from django.conf import settings


@shared_task()
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

@shared_task
def export_data(serialized_data,file_path):
    df = pd.DataFrame(serialized_data)
    df.to_csv(f'expert_portal/tribe/squad.csv', encoding='UTF-8', index=False)
    print(serialized_data)
    # response = HttpResponse(content_type='text/csv')
    # response["Content-Disposition"] = f'attachment; filename={file_name} '

    # with open(file_path, 'w', newline='') as file:
    #     # header = serialized_data[0].keys()
    #     header = ['name', 'squad_lead', 'members', 'date_created']
    #     # header = [field.name for field in serialized_data[0]['fields']]
    #     writer = csv.DictWriter(file, fieldnames=header)
    #     # writer.writerow()
    #     writer.writeheader

    #     for obj in serialized_data:
    #         writer.writerow(obj.values())

        # return response

# tasks.py
# from celery import shared_task
# import csv

# @shared_task
# def export_model_data_to_csv(serialized_data, file_path):
#     field_names = [field.name for field in serialized_data[0]['fields']]

#     with open(file_path, 'w', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(field_names)

#         for instance in serialized_data:
#             # writer.writerow([getattr(instance, field) for field in field_names])
#             writer.writerow([instance['fields'].get(field) for field in field_names])



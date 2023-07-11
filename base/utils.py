import smtplib
import csv

from django.http import HttpResponse

def export_data(serializer, file_name):

    response = HttpResponse(content_type='text/csv')
    response["Content-Disposition"] = f'attachment; filename={file_name} '

    writer = csv.writer(response)
    writer.writerow(serializer.child.fields.keys()) #get fieldnames from serializer field

    for obj in serializer.data:
        writer.writerow(obj.values())

    return response


import re

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Staff

def validate_email_domain(value):
    valid_email_domain = ("afexnigeria.com", "africaexchange.com", "afexkenya.com", "afexuganda.com", "afex.africa")
    if not value.endswith(valid_email_domain):
        raise serializers.ValidationError("Incorrect credentials.")
    return value

def validate_image_extension(value):

    allowed_extensions = ['png', 'jpeg', 'jpg']
    pattern = r'^.+\.({})$'.format('|'.join(allowed_extensions))
    if not re.match(pattern, value.name):
        raise serializers.ValidationError("Invalid file extension. Allowed extensions are: {}.".format(", ".join(allowed_extensions)))
    
unique_email = UniqueValidator(queryset=Staff.objects.all(), message="Email address already exists")
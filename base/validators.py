import re

from rest_framework import serializers

def validate_email_domain(value):
    valid_email_domain = ("afexnigeria.com", "africaexchange.com", "afexkenya.com", "afexuganda.com")
    if not value.endswith(valid_email_domain):
        raise serializers.ValidationError("Invalid email address. Enter your official email")
    return value

def validate_image_extension(value):

    allowed_extensions = ['png', 'jpeg', 'jpg']
    pattern = r'^.+\.({})$'.format('|'.join(allowed_extensions))
    if not re.match(pattern, value.name):

        raise serializers.ValidationError("Invalid file extension. Allowed extensions are: {}.".format(", ".join(allowed_extensions)))
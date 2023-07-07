from rest_framework import serializers

def validate_email_domain(value):
    domain = value.split("@")[1]
    valid_email_domain = ["afexnigeria.com", "africaexchange.com", "afexkenya.com", "afexuganda.com"]
    if not domain in valid_email_domain:
        raise serializers.ValidationError("Invalid email address. Enter your official email")
    return value
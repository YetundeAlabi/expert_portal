from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from .models import Staff, Admin

@receiver(pre_save, sender=Staff) #Signal to create unique identifier for staff
def generate_unique_identifier(sender, instance, **kwargs):
    if not instance.unique_id:
        random_digits = get_random_string(length=7, allowed_chars="0123456789")
        random_alphabet = get_random_string(length=1, allowed_chars="ABCDEFGHIJ")
        unique_id = f"{random_alphabet}{random_digits}"
        instance.unique_id = unique_id


@receiver(pre_save, sender=Admin)
def generate_unique_identifier(sender, instance, **kwargs):
    if not instance.unique_id:
        random_digits = get_random_string(length=7, allowed_chars="0123456789")
        random_alphabet = get_random_string(length=1, allowed_chars="ABCDEFGHIJ")
        unique_id = f"{random_alphabet}{random_digits}"
        instance.unique_id = unique_id

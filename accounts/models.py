from pytz import country_names

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from phonenumber_field.modelfields import PhoneNumberField

from base import constants
from base.models import BaseModel, DeletableBaseModel
from portal.models import Tribe, Squad
# Create your models here.

GENDER_CHOICES = [
        (constants.FEMALE, "Female"),
        (constants.MALE, "Male")
    ]

MARTIAL_STATUS_CHOICES = [
    (constants.DIVORCED, "Divorced"),
    (constants.MARRIED, "Married"),
    (constants.SINGLE, "Single"),
    (constants.WIDOWED, "Widowed"),
]

COUNTRY_CHOICES = [
    (code, country) for code, country in country_names.items()
]

class Staff(BaseModel, AbstractUser):
    
    id = models.CharField(max_length=8, unique=True)
    picture = models.ImageField(upload_to="accounts/media")
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    martial_status = models.CharField(max_length=20, choices=MARTIAL_STATUS_CHOICES)
    is_admin = models.BooleanField(default=False)
    alias_email = models.EmailField(max_length=255)
    tribe = models.ForeignKey(Tribe, on_delete=models.SET_NULL, null=True, related_name="staffs")
    squad = models.ForeignKey(Squad, on_delete=models.SET_NULL, null=True, related_name="members")
    role = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    work_phone = PhoneNumberField(blank=True)
    city = models.CharField(max_length=100)
    next_of_kin_first_name = models.CharField(max_length=150)
    next_of_kin_last_name = models.CharField(max_length=150)
    next_of_kin_middle_name = models.CharField(max_length=150, blank=True, null=True)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    next_of_kin_phone_number = PhoneNumberField(blank=True)
    next_of_kin_email = models.EmailField(max_length=255)
    next_of_kin_relationship = models.CharField(max_length=150)


@receiver(pre_save, sender=Staff)
def generate_unique_identifier(sender, instance, **kwargs):
    if not instance.id:
        random_digits = get_random_string(length=7, allowed_chars="0123456789")
        random_alphabet = get_random_string(length=1, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        id = f"{random_alphabet}{random_digits}"
        instance.id = id



#




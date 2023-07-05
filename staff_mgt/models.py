from pytz import country_names

from django.db import models

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

from base import constants
from base.models import BaseModel, DeletableBaseModel


User= get_user_model()

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


class Tribe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # lead = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, unique=True)
    lead = models.CharField(max_length=150)

    def get_staff_count(self):
        self.staffs.count()


class Squad(BaseModel):
    name = models.CharField(max_length=255)
    lead = models.CharField(max_length=150)
    # lead = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, unique=True)

   
    def get_member_count(self):
        return self.members.count()
    
    @property
    def description(self):
        pass


class StaffBaseModel(BaseModel):
    id = models.CharField(max_length=8, unique=True, primary_key=True)
    picture = models.ImageField(upload_to="accounts/media")
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    martial_status = models.CharField(max_length=20, choices=MARTIAL_STATUS_CHOICES)
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

    class Meta:
        abstract = True


@receiver(pre_save, sender=StaffBaseModel)
def generate_unique_identifier(sender, instance, **kwargs):
    if not instance.id:
        random_digits = get_random_string(length=7, allowed_chars="0123456789")
        random_alphabet = get_random_string(length=1, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        id = f"{random_alphabet}{random_digits}"
        instance.id = id


class Staff(StaffBaseModel):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=255)

    class Meta:
        indexes = [
            models.Index(fields=["last_name", "first_name", "email"]),
        ]

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'


class Admin(StaffBaseModel, User):
   pass
   

class Region(models.Model):
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)


class OfficeAddress(DeletableBaseModel):
    country = models.ForeignKey(Region, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    
    is_headquarter = models.BooleanField(default=False)
    

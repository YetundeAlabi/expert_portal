from pytz import country_names

from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

from base.constants import FEMALE, MALE, DIVORCED, MARRIED, SINGLE, WIDOWED
from base.models import BaseModel, DeletableBaseModel


User= get_user_model()

GENDER_CHOICES = [
        (FEMALE, FEMALE),
        (MALE, MALE)
    ]

MARTIAL_STATUS_CHOICES = [
    (DIVORCED, DIVORCED),
    (MARRIED, MARRIED),
    (SINGLE, SINGLE),
    (WIDOWED, WIDOWED),
]

COUNTRY_CHOICES = [
    (code, country) for code, country in country_names.items()
]


class Tribe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # tribe_lead = models.CharField(max_length=150)
    tribe_lead = models.ForeignKey("Staff", on_delete=models.SET_NULL, null=True)

    def get_staff_count(self):
       return self.staff_set.count()
    
    def get_squad_count(self):
        return self.squads.count()

    def __str__(self):
        return self.name


class Squad(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # squad_lead = models.CharField(max_length=150)
    tribe = models.ForeignKey(Tribe, on_delete=models.SET_NULL, null=True, related_name="squads")
    squad_lead = models.ForeignKey("Staff", on_delete=models.SET_NULL, null=True, related_name="squad_lead")

    def get_member_count(self):
        return self.staff_set.count()
    
    def __str__(self):
        return self.name


class StaffBaseModel(BaseModel):
    unique_id = models.CharField(max_length=8, null=True, blank=True, editable=False)
    picture = models.ImageField(upload_to="accounts/media")
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    martial_status = models.CharField(max_length=20, choices=MARTIAL_STATUS_CHOICES)
    alias_email = models.EmailField(max_length=255)
    tribe = models.ForeignKey(Tribe, on_delete=models.SET_NULL, null=True, blank=True)
    squad = models.ForeignKey(Squad, on_delete=models.SET_NULL, null=True, blank=True)
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
        

class Staff(StaffBaseModel):
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=["last_name", "first_name", "email"]),
        ]
    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def get_absolute_url(self):
        return reverse('staff_detail', args=[str(self.id)])
    
    @property
    def status(self):
        return self.is_active

"""Signal to create unique identifier for staff"""
@receiver(pre_save, sender=Staff)
def generate_unique_identifier(sender, instance, **kwargs):
    print(sender, instance)
    if not instance.unique_id:
        random_digits = get_random_string(length=7, allowed_chars="0123456789")
        random_alphabet = get_random_string(length=1, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        unique_id = f"{random_alphabet}{random_digits}"
        instance.unique_id = unique_id


class Admin(StaffBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   
    class Meta:
        indexes = [
            models.Index(fields=["last_name", "first_name", "email"]),
        ]

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

@receiver(pre_save, sender=Admin)
def generate_unique_identifier(sender, instance, **kwargs):
    print(sender, instance)
    if not instance.unique_id:
        random_digits = get_random_string(length=7, allowed_chars="0123456789")
        random_alphabet = get_random_string(length=1, allowed_chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        unique_id = f"{random_alphabet}{random_digits}"
        instance.unique_id = unique_id

   
class Region(models.Model):
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)

    def __str__(self):
        return self.country


class OfficeAddress(DeletableBaseModel):
    country = models.ForeignKey(Region, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    city = models.CharField(max_length=50, db_index=True)
    is_headquarter = models.BooleanField(default=False)
    
    def __str__(self):
        return self.country

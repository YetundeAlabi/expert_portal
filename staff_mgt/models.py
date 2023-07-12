from pytz import country_names

from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model


from phonenumber_field.modelfields import PhoneNumberField

from base.managers import ActiveUserManager
from base.models import BaseModel
from base.constants import FEMALE, MALE, DIVORCED, MARRIED, SINGLE, WIDOWED

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


class StaffBaseModel(BaseModel):
    unique_id = models.CharField(max_length=8, null=True, blank=True, editable=False)
    picture = models.ImageField(upload_to="media/", )
    middle_name = models.CharField(max_length=150, blank=True, null=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    martial_status = models.CharField(max_length=20, choices=MARTIAL_STATUS_CHOICES)
    alias_email = models.EmailField(max_length=255)
    tribe = models.ForeignKey('tribe.Tribe', on_delete=models.SET_NULL, null=True, blank=True) #to avoid circular import error
    squad = models.ForeignKey('tribe.Squad', on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    work_phone = PhoneNumberField(blank=True)
    city = models.ForeignKey('offices.City', on_delete=models.SET_NULL, null=True)
    next_of_kin_first_name = models.CharField(max_length=150)
    next_of_kin_last_name = models.CharField(max_length=150)
    next_of_kin_middle_name = models.CharField(max_length=150, blank=True, null=True)
    country = models.ForeignKey("offices.Country", on_delete=models.SET_NULL, null=True)
    next_of_kin_phone_number = PhoneNumberField(blank=True)
    next_of_kin_email = models.EmailField(max_length=255)
    next_of_kin_relationship = models.CharField(max_length=150)
    
    class Meta:
        abstract = True
        

class Staff(StaffBaseModel):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    suspension_date = models.DateField(blank=True, null=True)

    active_objects = ActiveUserManager()
    objects = models.Manager()

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


@receiver(pre_save, sender=Staff) #Signal to create unique identifier for staff
def generate_unique_identifier(sender, instance, **kwargs):
    if not instance.unique_id:
        random_digits = get_random_string(length=7, allowed_chars="0123456789")
        random_alphabet = get_random_string(length=1, allowed_chars="ABCDEFGHIJ")
        unique_id = f"{random_alphabet}{random_digits}"
        instance.unique_id = unique_id


class Admin(StaffBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

@receiver(pre_save, sender=Admin)
def generate_unique_identifier(sender, instance, **kwargs):
    if not instance.unique_id:
        random_digits = get_random_string(length=7, allowed_chars="0123456789")
        random_alphabet = get_random_string(length=1, allowed_chars="ABCDEF")
        unique_id = f"{random_alphabet}{random_digits}"
        instance.unique_id = unique_id


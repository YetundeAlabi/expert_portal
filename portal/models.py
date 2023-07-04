from pytz import country_names

from django.db import models

from base.models import BaseModel, DeletableBaseModel
from accounts.models import Staff
# Create your models here.
"""
create tribe, squad, ativity log and office address
"""

class Tribe(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    lead = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, unique=True)

class Squad(BaseModel):
    name = models.CharField(max_length=255)
    lead = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, unique=True)

    def limit_choices(self):
        return {"squad": self}
    
    def get_squad_count(self):
        return 
    @property
    def description(self):
        pass

class OfficeAddress(DeletableBaseModel):
    COUNTRY_CHOICES = [
        (code, country) for code, country in country_names.items()
    ]
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    
    is_headquarter = models.BooleanField(default=False)
    


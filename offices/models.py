from django.db import models

from base.constants import NIGERIA, KENYA, UGANDA, UNITED_STATES
from base.models import DeletableBaseModel

COUNTRY_CHOICES = [
    (NIGERIA, NIGERIA),
    (UGANDA, UGANDA),
    (KENYA, KENYA),
    (UNITED_STATES, UNITED_STATES),
]

class Country(models.Model):
    name = models.CharField(max_length=50,choices=COUNTRY_CHOICES, db_index=True)

    def __str__(self):
        return self.name
  

class City(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, related_name="cities")

    def __str__(self):
        return self.name
    

class Location(DeletableBaseModel):
    description = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    latitude = models.CharField(max_length=20)
    longitude = models.CharField(max_length=20)
    is_headquarter = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.city},{self.country}'

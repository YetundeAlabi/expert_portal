# from pytz import country_names

# from django.db import models


# from base.models import BaseModel, DeletableBaseModel
# from staff_mgt.models import COUNTRY_CHOICES

# # Create your models here.


# class Tribe(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     lead = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, unique=True)


# class Squad(BaseModel):
#     name = models.CharField(max_length=255)
#     lead = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, unique=True)

#     def limit_choices(self):
#         return {"squad": self}
    
#     def get_squad_count(self):
#         return 
#     @property
#     def description(self):
#         pass


# class OfficeAddress(DeletableBaseModel):
#     country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
#     latitude = models.CharField(max_length=20, blank=True, null=True)
#     longitude = models.CharField(max_length=20, blank=True, null=True)
#     city = models.CharField(max_length=150)
    
#     is_headquarter = models.BooleanField(default=False)
    
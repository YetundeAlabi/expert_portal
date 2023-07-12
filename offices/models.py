# from pytz import country_names

# from django.db import models

# from base.constants import NIGERIA, KENYA, UGANDA, UNITED_STATES
# from base.models import DeletableBaseModel

# # COUNTRY_CHOICES = [
# #     (NIGERIA, NIGERIA),
# #     (UGANDA, UGANDA),
# #     (KENYA, KENYA),
# #     (UNITED_STATES, UNITED_STATES),
# # ]

# COUNTRY_CHOICES = [
#     (code, country) for code, country in country_names.items()
# ]

# class Region(models.Model):
#     name = models.CharField(max_length=50,choices=COUNTRY_CHOICES, db_index=True)

#     def __str__(self):
#         return self.name
  


# from django.db import models

# from base.models import BaseModel


# class Tribe(BaseModel):
#     name = models.CharField(max_length=255, unique=True, db_index=True)
#     description = models.TextField()
#     # tribe_lead = models.ForeignKey("staff_mgt.Staff", on_delete=models.SET_NULL, null=True, blank=True, related_name="tribe_lead")

#     def get_staff_count(self):
#        return self.staff_set.count()
    
#     def get_squad_count(self):
#         return self.squads.count()

#     def __str__(self):
#         return self.name


# class Squad(BaseModel):
#     name = models.CharField(max_length=255, unique=True, db_index=True) 
#     description = models.TextField()
#     tribe = models.ForeignKey(Tribe, on_delete=models.SET_NULL, null=True, related_name="squads")
#     # squad_lead = models.ForeignKey("staff_mgt.Staff", on_delete=models.SET_NULL, blank = True, null=True, related_name="squad_lead")

#     def get_member_count(self):
#         return self.staff_set.count()
    
#     def __str__(self):
#         return self.name

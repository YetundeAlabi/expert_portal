from django.db import models

from .managers import ActiveManager, DeletedManager

class BaseModel(models.Model):
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)

   
    
    class Meta:
        abstract = True
        ordering = ["-date_created"]


class DeletableBaseModel(BaseModel):
    is_deleted = models.BooleanField(default=False)

    objects = models.Manager()
    active_objects = ActiveManager()
    deleted_objects = DeletedManager()

    class Meta:
        abstract = True
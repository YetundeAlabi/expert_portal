from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """ Creates and save new user"""
        if not email:
            raise ValueError("Email address is required")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """ creates superuser"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class ActiveUserManager(models.Manager):
   def get_queryset(self):
       return super().get_queryset().filter(is_active=True)


class ActiveManager(models.Manager):
 def get_queryset(self):
    return super(ActiveManager, self).get_queryset().filter(is_deleted=False)


class DeletedManager(models.Manager):
 def get_queryset(self):
    return super(DeletedManager, self).get_queryset().filter(is_deleted=True)
 
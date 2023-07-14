from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from base.managers import UserManager
from base.constants import CREATED, UPDATED, DELETED, UNREAD, READ

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model """
    email = models.EmailField(
        verbose_name="email address", max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True) #sign up required for only admin 
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    verification_code = models.CharField(max_length=7, blank=True, null=True)

    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    @property
    def is_admin(self):
        return self.is_staff

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        indexes = [
            models.Index(fields=["last_name", "first_name", "email"]),
        ]


ACTION_TYPES = [
    (CREATED, CREATED),
    (UPDATED, UPDATED),
    (DELETED, DELETED),  
]

ACTION_STATUS = [(UNREAD, UNREAD), (READ, READ)]

class ActivityLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    action_type = models.CharField(choices=ACTION_TYPES, max_length=15)
    action_time = models.DateTimeField(auto_now_add=True)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(choices=ACTION_STATUS, max_length=7)
    content_type = models.ForeignKey(
        ContentType, models.SET_NULL, blank=True, null=True
    )
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return f"{self.actor} {self.action_type}  on {self.action_time}"

    class Meta:
        ordering = ['-action_time']
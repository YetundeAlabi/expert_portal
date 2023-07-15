import logging

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from rest_framework.exceptions import ValidationError

from accounts.models import ActivityLog
from base.constants import SUCCESS, FAILED, CREATED, UPDATED, DELETED


class ActivityLogMixin:
    """Mixin to track user actions"""
    log_message = None

    def _get_action_type(self, request):
        return self.action_type_mapper().get(f"{request.method}")
    
    def _build_log_message(self, request):
        return f"User: {self._get_user(request)} -- Action Type: {self._get_action_type(request)}"
    
    def get_log_message(self, request) -> str:
        return self.log_message or self._build_log_message(request)

    @staticmethod
    def action_type_mapper():
        return {
            "POST": CREATED,
            "PUT": UPDATED,
            "PATCH": UPDATED,
            "DELETE": DELETED,
        }
    
    @staticmethod
    def _get_user(request):
        return request.user if request.user.is_authenticated else None
    
    def _write_log(self, request, response):
        status = SUCCESS if response.status_code < 400 else FAILED
        actor = self._get_user(request)

        data = {
            "actor": actor,
            "action_type": self._get_action_type(request),
            "status": status,
            "remarks": self.get_log_message(request),
        }
        try:
            data["content_type"] = ContentType.objects.get_for_model(
                self.get_queryset().model
            )
            data["content_object"] = self.get_object()
        except (AttributeError, ValidationError):
            data["content_type"] = None
        except AssertionError:
            pass

        ActivityLog.objects.create(**data)

    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        self._write_log(request, response)
        return response
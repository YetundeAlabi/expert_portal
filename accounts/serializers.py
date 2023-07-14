from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers

from staff_mgt import validators
from .models import ActivityLog
from base.constants import CREATED, UPDATED, DELETED, UNREAD, READ


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "first_name","last_name", "is_active"]
        

class UserLoginSerializer(serializers.ModelSerializer):
    """Serializer to authenticate users with email and password"""
    email = serializers.EmailField(validators=[validators.validate_email_domain])
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ("email", "password")

    def validate(self, validated_data):
        user = authenticate(**validated_data)
        if user.is_admin:
            if not user.is_active:
                raise serializers.ValidationError("You have been suspended")
            return user
        raise serializers.ValidationError("Incorrect Credentials")

    
class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(validators=[validators.validate_email_domain])


class VerifyPinSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validators.validate_email_domain])
    verification_code = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "verification_code"]


class ResetPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[validators.validate_email_domain])
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "new_password", "confirm_password"]

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs


class ActivityLogSerializer(serializers.ModelSerializer):
    actor = serializers.CharField(source='actor.get_full_name')
    action = serializers.SerializerMethodField()
    date_created = serializers.SerializerMethodField()
    
    class Meta:
        model = ActivityLog
        fields = ['id', 'actor', 'action_time', 'status', 'action', 'date_created']

    def get_action(self, obj):
        if obj.action_type == UPDATED:
            if obj.content_type.model == 'staff':
                return f"{obj.action_type} {obj.content_object.staff.get_full_name()}'s profile"
        elif obj.action_type == CREATED:
            if obj.content_type.model == 'squad':
                return f"{obj.action_type} a new squad {obj.content_object.name}"
            elif obj.content_type.model == 'officeaddress':
                return f"{obj.action_type} a new office address"
            elif obj.content_type.model == 'tribe':
                return f"A new tribe was {obj.action_type} {obj.content_object.name}"
    
    def get_date_created(self, obj):
        return obj.action_time.date().isoformat()
from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers

from base import validators

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
    email = serializers.EmailField()


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
        fields = ["new_password", "confirm_password"]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

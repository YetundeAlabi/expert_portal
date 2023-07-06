from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "password", "passsword2", "first_name","last_name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def validate_email(self, value):
        domain = value.split("@")[1]
        valid_email_domain = ["afexnigeria.com", "africaexchange.com", "afexkenya.com", "afexuganda.com"]
        if not domain in valid_email_domain:
            raise serializers.ValidationError("Invalid email address. Enter official email")
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs
    

class UserLoginSerializer(serializers.ModelSerializer):
    """Serializer to authenticate users with email and password"""
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "password")

    def validate(self, validated_data):
        user = authenticate(**validated_data)

        if user.is_admin and user.is_active:
            return user
        raise serializers.ValidationError("Incorrect Credentials")


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyPinSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    verication_code = serializers.CharField()

    class Meta:
        model = User
        fields = ["email", "verification_code"]
from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "password", "first_name","last_name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    # def validate_email(self, attrs):
    #     # return super().validate(attr

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

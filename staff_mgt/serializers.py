from datetime import datetime

from django.utils import timezone

from rest_framework import serializers
from rest_framework.reverse import reverse
from base import validators
from staff_mgt.models import Staff, Admin
from accounts.serializers import UserSerializer

# today = timezone.now().date()

class StaffSerializer(serializers.ModelSerializer):
    """Seriaizer for creating and updating staff"""
    email = serializers.EmailField(validators=[validators.validate_email_domain])
    picture = serializers.ImageField(validators=[validators.validate_image_extension])
    # is_active = serializers.BooleanField(read_only=True)
    # suspension_date = serializers.DateField(read_only=True)

    class Meta:
        model = Staff
        read_only_fields = ["id", "unique_id", "is_active", "suspension_date"]
        fields = "__all__"
        

class StaffListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Staff
        fields = ["name", "email", "phone_number", "tribe", "squad", "status",
                  "url", "id", "unique_id"]

    def get_name(self, obj):
        return obj.get_full_name()
    
    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("staff_mgt:staff_retrieve_update", kwargs={"pk": obj.pk}, request=request)


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = "__all__"
        read_only_fields = ["id", "unique_id"]
        

class SuspendStaffSerializer(serializers.Serializer):
    suspension_date = serializers.DateField(required=False)

    # def valid_suspension_date(self, value):
    #     if value <= timezone.now().date():
    #         raise serializers.ValidationError('suspension date cannot be later than today')
    #     return value

    def validate_suspension_date(self, value):
         # Convert datetime.date to string
        value_str = value.strftime('%Y-%m-%d')
        # Check if the value is in the expected format 'YYYY-MM-DD'
        try:
            datetime.strptime(value_str, '%Y-%m-%d')
            # if value <= datetime.now().date():
            #     raise serializers.ValidationError('suspension date cannot be later than today')
        except ValueError:
            raise serializers.ValidationError("Invalid date format. It must be in YYYY-MM-DD format.")
        
        return value_str


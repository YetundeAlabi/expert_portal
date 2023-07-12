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

    class Meta:
        model = Staff
        read_only_fields = ["id", "unique_id"]
        exclude = ["is_active"]
        

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
    suspension_date = serializers.DateTimeField(required=False)

    def valid_suspension_date(self, value):
        if value <= timezone.now().date():
            raise serializers.ValidationError('suspension date cannot be later than today')
        return value




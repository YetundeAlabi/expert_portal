from datetime import datetime

from rest_framework import serializers
from rest_framework.reverse import reverse

from staff_mgt.validators import validate_email_domain, unique_email, validate_image_extension
from staff_mgt.models import Staff, Admin
from accounts.serializers import UserSerializer


class StaffSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating staff
    """
    email = serializers.EmailField(validators=[validate_email_domain, unique_email])
    alias_email = serializers.EmailField(validators=[validate_email_domain, unique_email])
    picture = serializers.ImageField(validators=[validate_image_extension])
   
    class Meta:
        model = Staff
        read_only_fields = ["id", "unique_id", "is_active", "suspension_date"]
        fields = "__all__"
        

class StaffListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    tribe = serializers.CharField(source="tribe.name", read_only=True)
    squad = serializers.CharField(source="squad.name", read_only=True)

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

    def validate_suspension_date(self, value):
        value_str = value.strftime('%Y-%m-%d')# Convert datetime.date to string
        try:
            datetime.strptime(value_str, '%Y-%m-%d')
            if value <= datetime.now().date():
                raise serializers.ValidationError('Suspension date cannot be later than today')
        except ValueError:
            raise serializers.ValidationError("Invalid date format. It must be in YYYY-MM-DD format.")
        
        return value_str


class ExportStaffIdSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField())
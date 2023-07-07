
from rest_framework import serializers
from rest_framework.reverse import reverse
from base import validators
from staff_mgt.models import Staff, Admin
from accounts.serializers import UserSerializer

class StaffSerializer(serializers.ModelSerializer):
    """Seriaizer for creating and updating staff"""
    email = serializers.EmailField(validators=[validators.validate_email_domain])

    class Meta:
        model = Staff
        read_only_fields = ["id", "unique_id"]
        exclude = ["is_active"]


class StaffListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    detail_url = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Staff
        fields = ["name", "email", "phone_number", "tribe", "squad", "status",
                  "detail_url", "edit_url", "id", "unique_id"]

    def get_name(self, obj):
        return obj.get_full_name()
    
    def get_detail_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("staff_mgt:staff_detail", kwargs={"pk": obj.pk}, request=request)

    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("staff_mgt:staff_edit", kwargs={"pk": obj.pk}, request=request)



class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = "__all__"
        read_only_fields = ["id", "unique_id"]
        

class SuspendStaffSerializer(serializers.Serializer):
    suspension_date = serializers.DateField()



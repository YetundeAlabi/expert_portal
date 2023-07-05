from django.urls import reverse

from rest_framework import serializers

from staff_mgt.models import Staff, Admin
from accounts.serializers import UserSerializer

class StaffSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Staff
        fields = ["first_name", "last_name", "email", "picture", "middle_name", "date_of_birth", "gender",
                  "martial_status", "picture", "alias_email", "squad", "role",
                    "phone_number", "work_phone", "city", "next_of_kin_first_name",
                    "next_of_kin_last_name", "next_of_kin_middle_name", "country",
                    "next_of_kin_phone_number", "next_of_kin_email", "next_of_kin_relationship"]
        
        read_only_fields = ["id", "unique_id"]

class StaffListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    staff_count = serializers.SerializerMethodField()
    update_url = serializers.HyperlinkedIdentityField(
        view_name="staff_update",
        lookup_field = "pk",
        read_only =True
    )
    # detail_url =
    # deactivate_url =

    class Meta:
        model = Staff
        fields = ["name", "email", "phone_number", "tribe", "squad", "status", "staff_count", "update_url",
                  "detail_url", "deactivate_url"]

    def get_name(self, obj):
        return obj.get_full_name()
    
    def get_staff_count(self):
        return Staff.objects.count()


class AdminSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Admin
        fields = ["picture", "middle_name", "date_of_birth", "gender",
                  "martial_status", "picture", "alias_email", "squad", "role",
                    "phone_number", "work_phone", "city", "next_of_kin_first_name",
                    "next_of_kin_last_name", "next_of_kin_middle_name", "country",
                    "next_of_kin_phone_number", "next_of_kin_email", "next_of_kin_relationship", "user"]




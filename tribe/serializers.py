from django.urls import reverse

from rest_framework import serializers

from staff_mgt.models import Tribe, Squad, Region, OfficeAddress, Staff
from accounts.serializers import UserSerializer


class SquadListSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    edit_url = serializers.SerializerMethodField()
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="squad_detail",
        lookup_field = "pk",
        read_only =True
    )
    class Meta:
        model = Squad
        fields= ["name", "squad_lead", "member_count", "date_created", "edit_url", "detail_url"]

    def get_member_count(self, obj):
        return obj.get_member_count()
                                                                                                                        
    def get_edit_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("squad_update", kwargs={"pk": obj.pk}, request=request)


class TribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tribe
        fields = ["name", "description", "tribe_lead"]

    def validate_tribe_lead(self, value):
        """ check that squad lead exists in the tribe"""
        qs = Tribe.staff_set.filter(pk=value).exist()
        if not qs:
            raise serializers.ValidationError({"message": "Staff is not a member of this tribe"})
        return value


class TribeListSerializer(serializers.ModelSerializer):
    squads = serializers.StringRelatedField(many=True, read_only=True) #get names of squads in a tribe 
    edit_url = serializers.HyperlinkedIdentityField(
        view_name="tribe_update",
        lookup_field = "pk",
        read_only =True
    )
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="tribe_detail",
        lookup_field = "pk",
        read_only =True
    )

    class Meta:
        model = Tribe
        fields = ["name", "tribe_lead", "date_created", "edit_url", "detail_url"]


class TribeDetailSerializer(serializers.ModelSerializer):
    num_squads = serializers.SerializerMethodField()
    overall_squad_members = serializers.SerializerMethodField() 
    staff_members = serializers.SerializerMethodField() 
    squad = SquadListSerializer()

    class Meta:
        fields = ["name", "description", "tribe_lead", "num_squads", "overall_squad_members", "squad"]

    def get_num_squads(self, obj):
        return obj.get_staff_count()
    
    def get_overall_squad_members(self, obj):
        return obj.get_staff_set.count()
    
    def get_staff_members(self, obj):
        return Staff.objects.filter(tribe=obj).count()
    


class SquadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Squad
        fields = ["name", "description", "squad_lead"]

    def validate_squad_lead(self):
        pass


class RegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ["country"]


class OfficeAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeAddress
        fields = ["country", "latitude", "longitude", "city", "is_headquarter", "description"]


class OfficeAddressListSerializer(serializers.ModelSerializer):
    # edit_url
    # delete

    class Meta:
        model = OfficeAddress
        fields = ["country", "city", "is_headquarter", "description"]

   

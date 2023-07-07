
from rest_framework.reverse import reverse
from rest_framework import serializers

from staff_mgt.models import Tribe, Squad, Region, Location, Staff
from accounts.serializers import UserSerializer


class SquadListSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Squad
        fields= ["name", "squad_lead", "members", "date_created", "url"]

    def get_members(self, obj):
        print(obj)
        return obj.staff_set.count()
                                                                                                                        
    def get_url(self, obj):
        request = self.context.get('request')
        tribe_id = self.context.get('tribe_id')
        if request is None:
            return None
        return reverse("tribe:squad_detail_update", kwargs={"pk": obj.pk, "tribe_pk": tribe_id}, request=request)


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
    url = serializers.SerializerMethodField()

    class Meta:
        model = Tribe
        fields = ["name", "tribe_lead", "date_created", "url", "squads"]

    def get_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return reverse("tribe:tribe_detail_update", kwargs={"pk": obj.pk}, request=request)


class TribeDetailSerializer(serializers.ModelSerializer):
    num_squads = serializers.SerializerMethodField()
    overall_squad_members = serializers.SerializerMethodField() 
    staff_members = serializers.SerializerMethodField() 
    # squads = SquadListSerializer()

    class Meta:
        model = Tribe
        fields = ["name", "description", "tribe_lead", "num_squads", "overall_squad_members", "staff_members"]

    def get_num_squads(self, obj):
        return obj.get_staff_count()
    
    def get_overall_squad_members(self, obj):
        return obj.get_squad_count()
    
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


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ["country", "latitude", "longitude", "city", "is_headquarter", "description"]


class LocationListSerializer(serializers.ModelSerializer):
    # edit_url
    delete_url = serializers.HyperlinkedIdentityField(
        view_name="delete_location",
        lookup_field = "pk",
        read_only =True
    )

    edit_url = serializers.HyperlinkedIdentityField(
        view_name="location_update",
        lookup_field = "pk",
        read_only =True
    )
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="location_detail",
        lookup_field = "pk",
        read_only =True
    )


    class Meta:
        model = Location
        fields = ["country", "city", "is_headquarter", "description", "edit_url", "detail_url", "delete_url"]

   
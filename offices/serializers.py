from rest_framework.reverse import reverse
from rest_framework import serializers

from staff_mgt.models import Region, OfficeAddress


class RegionSerializer(serializers.ModelSerializer):
    # list country prefetched with cities
    class Meta:
        model = Region
        fields = ["name"]


class OfficeCityAddressSerializer(serializers.ModelSerializer):
    country = RegionSerializer()

    class Meta:
        model = OfficeAddress
        fields = ["city"]
  

class OfficeAddressSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    
    class Meta:
        model = OfficeAddress
        fields = ["latitude", "longitude", "region", "city", "is_headquarter", "description"]

    def create(self, validated_data):
        region = validated_data.pop("region")
        region_id = self.context.get('region_id')
        return OfficeAddress.objects.create(**validated_data, region_id=region_id)


class OfficeAddressListSerializer(serializers.ModelSerializer):
    # edit_url
    delete_url = serializers.HyperlinkedIdentityField(
        view_name="delete_office_address",
        lookup_field = "pk",
        read_only =True
    )

    edit_url = serializers.HyperlinkedIdentityField(
        view_name="update_office_address",
        lookup_field = "pk",
        read_only =True
    )

    detail_url = serializers.HyperlinkedIdentityField(
        view_name="OfficeAddress_detail",
        lookup_field = "pk",
        read_only =True
    )

    class Meta:
        model = OfficeAddress
        fields = ["is_headquarter", "description", "edit_url", "detail_url", "delete_url"]

 
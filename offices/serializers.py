from rest_framework.reverse import reverse
from rest_framework import serializers

from offices.models import Country, Location, City


class CountrySerializer(serializers.ModelSerializer):
    # list country prefetched with cities
    class Meta:
        model = Country
        fields = ["name"]


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = City
        fields = ["country", "name"]

    def create(self, validated_data):
        country_id = self.context.get('country_id')
        return City.objects.create(**validated_data, country_id=country_id)


class CityListSerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ["name"]
        

class LocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Location
        fields = ["latitude", "longitude", "country", "city", "is_headquarter", "description"]


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
        fields = ["is_headquarter", "description", "edit_url", "detail_url", "delete_url"]

 
from rest_framework.reverse import reverse
from rest_framework import serializers

from tribe.models import Tribe, Squad
from staff_mgt.models import Staff

class SquadListSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    
    class Meta:
        model = Squad
        fields= ["name", "squad_lead", "members", "date_created", "url"]

    def get_members(self, obj):
        return obj.staff_set.count()
                                                                                                                        
    def get_url(self, obj):
        request = self.context.get('request')
        tribe_id = self.context.get('tribe_id')
        if request is None:
            return None
        return reverse("tribe:squad_detail_update", kwargs={"pk": obj.pk, "tribe_pk": tribe_id}, request=request)


class ExportSquadSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()
    date_created = serializers.SerializerMethodField()
    
    class Meta:
        model = Squad
        fields= ["name", "squad_lead", "members", "date_created"]

    def get_members(self, obj):
        return obj.staff_set.count()

    def get_date_created(self, obj):
        return obj.date_created.date().isoformat()
        

class TribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tribe
        fields = ["name", "description", "tribe_lead"]

    def validate_tribe_lead(self, value):
        """ check that squad lead exists in the tribe"""
        tribe = self.instance
        if value is not None and value.tribe != tribe:
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
        fields = ["id","name", "description", "squad_lead"]
        read_only_field = ["id"]

    def validate_squad_lead(self, value):
        squad = self.instance
        if value is not None and value.squad != squad:
            raise serializers.ValidationError({"message": "Staff is not a member of this tribe"})
        return value
    
    def create(self, validated_data):
        tribe_id = self.context.get('tribe_id')
        return Squad.objects.create(**validated_data, tribe_id=tribe_id)


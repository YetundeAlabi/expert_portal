from rest_framework.generics import (
    DestroyAPIView, GenericAPIView, UpdateAPIView,
    ListAPIView, RetrieveUpdateAPIView
)
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status,filters

from staff_mgt.models import Tribe, Squad, Region, OfficeAddress
from base.mixins import ActivityLogMixin
from tribe import serializers
from base.utils import  export_data


class TribeCreateAPIView(ActivityLogMixin, GenericAPIView):
    queryset = Tribe.objects.all()
    serializer_class = serializers.TribeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tribe=serializer.save()
            self.created_obj = tribe #to get created_obj id in the activity log mixin
            data = serializer.data
            return Response({'message': 'Tribe created successfully', 'data': data}, 
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TribeListAPIView(ListAPIView):
    serializer_class = serializers.TribeListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "squads__name"]

    def get_queryset(self):
        return Tribe.objects.prefetch_related("squads")
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        tribe_count = queryset.count()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response({'message': 'Tribe list pulled successfully', 'data': data, 'tribe_count': tribe_count}, status=status.HTTP_200_OK) 


class TribeDetailUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Tribe.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.TribeDetailSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return serializers.TribeSerializer


class ExportTribeAPIView(GenericAPIView):
    queryset = Tribe.objects.all()
    serializer_class = serializers.TribeListSerializer

    def get(self, request, *args, **kwargs):
        model_name = self.get_serializer().Meta.model.__name__
        file_name = f'{model_name.lower()}.csv'
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        file = export_data(serializer=serializer, file_name=file_name)
        return file
    

class SquadDetailUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Squad.objects.all()
    serializer_class = serializers.SquadSerializer

    def get_queryset(self):
        tribe_pk = self.kwargs["tribe_pk"]
        return super().get_queryset().filter(tribe_id=tribe_pk)
    
    
class SquadListCreateAPIView(ActivityLogMixin, generics.ListCreateAPIView):
    queryset = Squad.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "tribe__name"]

    def get_queryset(self):
        tribe_pk = self.kwargs["tribe_pk"]
        return super().get_queryset().filter(tribe_id=tribe_pk)
        
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.SquadListSerializer
        return serializers.SquadSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["tribe_id"] = self.kwargs["tribe_pk"]
        context["request"] = self.request
        return context

    def perform_create(self, serializer):
        """ overiding this method to get created_obj id in the activity log mixin"""
        squad = serializer.save()
        self.created_obj = squad
        return Response({'message': 'Squad created succesfully'}, status=status.HTTP_201_CREATED)
    

class ExportSquadAPIView(GenericAPIView):
    serializer_class = serializers.ExportSquadSerializer

    def get_queryset(self):
        tribe_pk = self.kwargs["tribe_pk"]
        return Squad.objects.filter(tribe_id=tribe_pk)
    
    def get(self, request, *args, **kwargs):
        """
        get tribe and squad name as file name 
        e.g innovation_and_technology_squad.csv/ ACEL_squad.csv
        """
        tribe_pk = self.kwargs["tribe_pk"]
        tribe = Tribe.objects.get(pk=tribe_pk)
        tribe_name = tribe.name.replace(" ", "_")
        model_name = self.get_serializer().Meta.model.__name__
        file_name = f'{tribe_name}_{model_name}.csv' 
        file_name = file_name.lower()

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        file = export_data(serializer=serializer, file_name=file_name)
        return file


class CountryListAPIView(ListAPIView):
    queryset = Region.objects.all()
    serializer_class = serializers.RegionSerializer


class OfficeAddressListCreateAPIView(ActivityLogMixin, generics.ListCreateAPIView):
    queryset = OfficeAddress.objects.all()
    serializer_class = serializers.OfficeAddressSerializer
    lookup_field = 'pk'
    
    def get_queryset(self):
        region_pk = self.kwargs["region_pk"]
        return OfficeAddress.objects.filter(region_id=region_pk)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["region_id"] = self.kwargs["region_pk"]
        context["request"] = self.request
        return context
    
    def perform_create(self, serializer):
        """ overiding this method to get created_obj id in the activity log mixin"""
        office_address = serializer.save()
        self.created_obj = office_address
        return Response({'message': 'Office address created succesfully'}, status=status.HTTP_201_CREATED)

class OfficeAddressListAPIView(ListAPIView): 
    """
    Endpoint to list all offices address
    """
    serializer_class = serializers.OfficeAddressListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["city", "region__name"]

    def get_queryset(self):
        return OfficeAddress.active_objects.order_by("id").all()

         
class OfficeAddressUpdateAPIView(UpdateAPIView):
    queryset = OfficeAddress.objects.all()
    serializer_class = serializers.OfficeAddressSerializer
    lookup_field = 'pk'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class OfficeAddressDestroyAPIView(DestroyAPIView):
    queryset = OfficeAddress.objects.all()
    serializer_class = serializers.OfficeAddressSerializer
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "address has been deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])

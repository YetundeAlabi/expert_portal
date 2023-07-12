from rest_framework.generics import DestroyAPIView, UpdateAPIView, ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status, filters

from staff_mgt.models import Region, OfficeAddress
from base.mixins import ActivityLogMixin
from offices.serializers import  RegionSerializer, OfficeAddressSerializer, OfficeAddressListSerializer, OfficeCityAddressSerializer

# Create your views here.

# class CountryListAPIView(ActivityLogMixin, ListAPIView):
#     queryset = Country.objects.all()
#     serializer_class = CountrySerializer


class OfficeAddressCreateAPIView(ActivityLogMixin, CreateAPIView):
    queryset = OfficeAddress.objects.all()
    serilizer_class = OfficeAddressSerializer
    
    def get_queryset(self):
        region_pk = self.kwargs["region_pk"]
        return OfficeAddress.objects.filter(region_id=region_pk)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["region_id"] = self.kwargs["region_pk"]
        context["request"] = self.request
        return context


class OfficeAddressListAPIView(ActivityLogMixin, ListAPIView):
    serializer_class = OfficeAddressListSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["city", "region__name"]

    def get_queryset(self):
        return OfficeAddress.active_objects.all()

         
class OfficeAddressUpdateAPIView(ActivityLogMixin, UpdateAPIView):
    queryset = OfficeAddress.objects.all()
    serializer_class = OfficeAddressSerializer


class OfficeAddressDestroyAPIView(ActivityLogMixin, DestroyAPIView):
    queryset = OfficeAddress.objects.all()
    serializer_class = OfficeAddressSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "address has been deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])

from rest_framework.generics import DestroyAPIView, UpdateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status, filters

from offices.models import City, Location, Country
from base.mixins import ActivityLogMixin
from offices.serializers import  LocationSerializer, CitySerializer, LocationListSerializer, CityListSerializer, CountrySerializer

# Create your views here.

class CountryListAPIView(ActivityLogMixin, ListAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityListCreateAPIView(ActivityLogMixin, ListCreateAPIView):
    queryset = City.objects.all()
    
    def get_queryset(self):
        country_pk = self.kwargs["country_pk"]
        return City.objects.filter(country_id=country_pk)
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return CityListSerializer
        return CitySerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["country_id"] = self.kwargs["country_pk"]
        context["request"] = self.request
        return context


class LocationListCreateAPIView(ActivityLogMixin, ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["city__name", "country__name"]

    def get_queryset(self):
        if self.request.method == "GET":
            return self.queryset.active_objects.all()
        return super().get_queryset()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LocationListSerializer
        return LocationSerializer
   
         
class LocationUpdateAPIView(ActivityLogMixin, UpdateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationDestroyAPIView(ActivityLogMixin, DestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "address has been deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])

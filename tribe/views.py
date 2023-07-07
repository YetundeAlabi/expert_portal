from rest_framework.generics import RetrieveAPIView, GenericAPIView, UpdateAPIView, ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from staff_mgt.models import Tribe, Squad, Region, Location
from base.mixins import ActivityLogMixin
from tribe import serializers
from .serializers import SquadSerializer, SquadListSerializer,TribeSerializer,TribeListSerializer, RegionSerializer, LocationSerializer, TribeDetailSerializer
# from base.constants import FEMALE, MALE

# Create your views here.

class TribeCreateAPIView(ActivityLogMixin, GenericAPIView):
    queryset = Tribe.objects.all()
    serializer_class = TribeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response({'message': 'Tribe created successfully', 'data': data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TribeListAPIView(ActivityLogMixin, ListAPIView):
    serializer_class = TribeListSerializer

    def get_queryset(self):
        return Tribe.objects.prefetch_related("squads")
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        tribe_count = queryset.count()

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response({'message': 'Tribe list pulled successfully', 'data': data, 'tribe_count': tribe_count}, status=status.HTTP_200_OK) 


# class TribeDetailAPIView(RetrieveAPIView):
#     queryset = Tribe.objects.all()
#     serializer_class = TribeDetailSerializer


# class TribeUpdateAPIView(UpdateAPIView):
#     queryset = Tribe.objects.all()
#     serializer_class = TribeSerializer



class TribeDetailUpdateAPIView(ActivityLogMixin, RetrieveUpdateAPIView):
    queryset = Tribe.objects.all()
    lookup_field = 'pk'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TribeDetailSerializer
        elif self.request.method in ['PUT', 'PATCH']:
            return TribeSerializer


class SquadDetailUpdateAPIView(ActivityLogMixin, RetrieveUpdateAPIView):
    queryset = Squad.objects.all()
    serializer_class = SquadSerializer

    def get_queryset(self):
        tribe_pk = self.kwargs["tribe_pk"]
        return self.queryset.filter(tribe_id=tribe_pk)
    
    

class SquadListAPIView(ListAPIView):
    queryset = Squad.objects.all()
    serializer_class = SquadListSerializer

    def get_queryset(self):
        tribe_pk = self.kwargs["tribe_pk"]
        return self.queryset.filter(tribe_id=tribe_pk)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["tribe_id"] = self.kwargs["tribe_pk"]
        context["request"] = self.request
        return context


class RegionCreateAPIView(ActivityLogMixin, CreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class LocationCreateAPIView(ActivityLogMixin, CreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationUpdateAPIView(ActivityLogMixin, UpdateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class LocationListAPIView(ActivityLogMixin, ListAPIView):
    queryset = Location.objects.all()
    serializer_class = serializers.LocationListSerializer

    def get_queryset(self):
        return self.queryset.active_objects.all()


class LocationDestroyAPIView(ActivityLogMixin, generics.DestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "address has been deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])

    
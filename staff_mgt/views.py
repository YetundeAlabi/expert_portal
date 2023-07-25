from datetime import datetime

from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from rest_framework.generics import (GenericAPIView, ListAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.response import Response

from base.constants import FEMALE, MALE
from base.utils import export_data
from staff_mgt import serializers
from staff_mgt.models import Squad, Staff, Tribe


def latest_object(MyModel):
    now = timezone.now()
    latest_obj = MyModel.objects.latest("date_created").date_created

    days_ago = (now - latest_obj).days
    return days_ago
    

class DashboardAPIView(GenericAPIView):
    """ 
    An endpoint to get dashboard paramaters.
    """
    serializer_class = serializers.StaffListSerializer
    authentication_classes = ()
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        latest_tribe = latest_object(Tribe)
        latest_squad = latest_object(Squad)
        recent_staff = Staff.active_objects.order_by("-date_created")[:10]
        male_staff = Staff.objects.filter(gender=MALE).count()
        female_staff = Staff.objects.filter(gender=FEMALE).count()
        total_staff = Staff.objects.count()
        total_tribe =  Tribe.objects.count()
        total_squad = Squad.objects.count()
        serializer = self.get_serializer(recent_staff, many=True)
        recent_staff_data = serializer.data

        data = {
            "male_staff": male_staff,
            "female_staff": female_staff,
            "overall_staff": total_staff,
            "overall_tribe": total_tribe,
            "overall_squad": total_squad,
            "recent_staff": recent_staff_data,
            "last_created_tribe": f'{latest_tribe}d ago',
            "last_created_squad": f'{latest_squad}d ago',
        }

        return Response(data, status=status.HTTP_200_OK)


class StaffCreateAPIView(GenericAPIView):
    """
     Endpoint to create staff. 
    """
    queryset = Staff.objects.all()
    serializer_class = serializers.StaffSerializer
        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        return Response({'message': 'Staff created successfully', 'data': data}, status=status.HTTP_201_CREATED)
      

class StaffListAPIView(ListAPIView):
    """
    Endpoint to get list of all staff with their tribe and squad.
    """
    queryset = Staff.objects.all()
    serializer_class = serializers.StaffListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["tribe__name", "squad__name", "is_active"]
    search_fields = ["first_name", "last_name"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        staff_count = queryset.count()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return Response({'message': 'Staff list pulled successfully', 'data': data, 'staff_count': staff_count}, status=status.HTTP_200_OK) 


class StaffRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Staff.objects.all()
    serializer_class = serializers.StaffSerializer
    lookup_field = "pk"


class ExportStaffAPIView(GenericAPIView):
    """
    Endpoint to get selected staff as a csv. expects ids of the selected staff
    """
    queryset = Staff.objects.all()
    serializer_class = serializers.ExportStaffIdSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff_ids = serializer.validated_data['ids']
        model_name = self.get_serializer().Meta.model.__name__
        file_name = f'{model_name.lower()}.csv' 
        
        queryset = self.get_queryset.filter(id__in=staff_ids)
        serializer = serializers.StaffListSerializer(queryset, many=True)

        file = export_data(serializer=serializer, file_name=file_name)
        return file


class SuspendStaffAPIView(GenericAPIView):
    """
    Endpoint to activate and deactivate staff. Scheduled staff deactivation expects suspension date.
    """    
    queryset = Staff.objects.all()
    serializer_class = serializers.SuspendStaffSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        suspension_date = serializer.validated_data.get("suspension_date")
        instance = self.get_object()
        if suspension_date is None:
            instance.is_active = not instance.is_active
            instance.save(update_fields=["is_active"])
        else:
            #convert suspension_date to a string
            suspension_date_str = datetime.strptime(suspension_date, '%Y-%m-%d').date() 
            instance.suspension_date = suspension_date_str
            instance.save(update_fields=["suspension_date"])
            
        serializer = serializers.StaffSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
        

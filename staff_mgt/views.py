from datetime import datetime

from rest_framework.generics import RetrieveAPIView, GenericAPIView, UpdateAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework import status, filters
from django_filters.rest_framework import DjangoFilterBackend


from staff_mgt.models import Staff, Admin, Tribe, Squad
from base.mixins import ActivityLogMixin
from .serializers import StaffSerializer, StaffListSerializer, AdminSerializer, SuspendStaffSerializer
from base.constants import FEMALE, MALE
from base.utils import export_data


class DashboardAPIView(ActivityLogMixin, GenericAPIView):
    """ 
    An endpoint to get dashboard paramaters 
    """
    serializer_class = StaffListSerializer

    def get(self, request, *args, **kwargs):
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
        }

        return Response(data, status=status.HTTP_200_OK)


class StaffCreateAPIView(ActivityLogMixin, GenericAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response({'message': 'Staff created successfully', 'data': data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffListAPIView(ActivityLogMixin, ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["tribe", "squad", "is_active"]
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


class StaffRetrieveUpdateAPIView(ActivityLogMixin, RetrieveUpdateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    lookup_field = "pk"


class ExportStaffAPIView(GenericAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffListSerializer

    def get(self, request, *args, **kwargs):
        model_name = self.get_serializer().Meta.model.__name__
        file_name = f'{model_name.lower()}.csv'
        staff_ids = request.data.get('staff_ids', [])

        queryset = self.get_queryset.filter(id__in=staff_ids)
        # queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        file = export_data(serializer=serializer, file_name=file_name)
        return file


class AdminDetailAPIView(ActivityLogMixin, RetrieveAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer


class SuspendStaffAPIView(ActivityLogMixin, GenericAPIView):
    queryset = Staff.objects.all()
    serializer_class = SuspendStaffSerializer

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        suspension_date = serializer.validated_data.get("suspension_date")
        instance = self.get_object()
        if suspension_date is None:
            instance.is_active = not instance.is_active
            instance.save(update_fields=["is_active"])
        else:
            suspension_date_str = datetime.strptime(suspension_date, '%Y-%m-%d').date() #convert suspension_date to a string
            instance.suspension_date = suspension_date_str
            instance.save(update_fields=["suspension_date"])
            
        serializer = StaffSerializer(instance=instance)
        test = ~instance.is_active

        return Response({"data":serializer.data, "test": test,}, status=status.HTTP_200_OK)
        

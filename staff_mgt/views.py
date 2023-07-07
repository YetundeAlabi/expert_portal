from rest_framework.generics import RetrieveAPIView, GenericAPIView, UpdateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Staff, Tribe, Squad, Admin
from .serializers import StaffSerializer, StaffListSerializer, AdminSerializer
from base.constants import FEMALE, MALE


class DashboardAPIView(GenericAPIView):
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


class StaffCreateAPIView(GenericAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            return Response({'message': 'Staff created successfully', 'data': data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffListAPIView(ListAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffListSerializer

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


class StaffDetailAPIView(RetrieveAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class StaffUpdateAPIView(UpdateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    lookup_field = "pk"


class AdminDetailAPIView(RetrieveAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminSerializer


class SuspendStaffAPIView(UpdateAPIView):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    # def get_object(self):
    #     staff_id = self.kwargs['pk']
    #     return self.queryset.filter(pk=staff_id)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = not instance.is_active
        instance.save(update_fields=["is_active"])
        serializer = StaffSerializer(instance=instance, data=request.data)
        if serializer.is_valid():
            
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # instance = self.get_object()
        # instance.response = request.data.get('response', instance.response)
        # instance.is_responded = True
        # instance.save(update_fields=['response', 'is_responded'])
        # serializer = self.get_serializer(instance)
        # return Response(serializer.data, status=status.HTTP_200_OK)

from django.urls import path

from staff_mgt import views

app_name = "staff_mgt"
urlpatterns = [
    path("dashboard/", views.DashboardAPIView.as_view(), name="dashboard"),
    path("staff/create", views.StaffCreateAPIView.as_view(), name="create_staff"),
    path("staff/", views.StaffListAPIView.as_view(), name="staff_list"),
    path("staff/<int:pk>/", views.StaffRetrieveUpdateAPIView.as_view(), name="staff_retrieve_update"),
    path("staff/export", views.ExportStaffAPIView.as_view(), name="staff_export"),
    path("admin/<int:pk>/", views.AdminDetailAPIView.as_view(), name="admin-detail")
]

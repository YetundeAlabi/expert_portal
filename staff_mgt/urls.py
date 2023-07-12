from django.urls import path

from staff_mgt import views

app_name = "staff_mgt"
urlpatterns = [
    path("dashboard/", views.DashboardAPIView.as_view(), name="dashboard"),
    path("create", views.StaffCreateAPIView.as_view(), name="create_staff"),
    path("", views.StaffListAPIView.as_view(), name="staff_list"),
    path("<int:pk>/", views.StaffRetrieveUpdateAPIView.as_view(), name="staff_retrieve_update"),
    path("<int:pk>/suspend", views.SuspendStaffAPIView.as_view(), name="suspend_staff"),
    path("export", views.ExportStaffAPIView.as_view(), name="staff_export"),
    path("admin/<int:pk>/", views.AdminDetailAPIView.as_view(), name="admin-detail")
]

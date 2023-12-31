from django.urls import path

from . import views

app_name = "accounts"
urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("forget-password/", views.ForgetPasswordView.as_view(), name="forget_password"),
    path("verify-pin/", views.VerifyPinView.as_view(), name="verify_pin"),
    path("reset-password/", views.ResetPasswordView.as_view(), name="reset-password"),
    path("activity-log/", views.ActivityLogAPIView.as_view(), name='activity_log'),
    path("activity-log/sorted", views.ActivityLogSortAPIView.as_view(), name='activity_log'),
    path("activity-log/export", views.ExportActivityLogAPIView.as_view(), name='export_activity_log')
]

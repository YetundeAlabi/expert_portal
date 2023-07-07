from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("forget-password/", views.ForgetPasswordView.as_view(), name="forget_password"),
    path("verify-pin/", views.VerifyPinView.as_view(), name="verify_pin")
]

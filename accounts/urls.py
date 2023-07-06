from django.urls import path

from accounts.views import LoginAPIView, LogoutView

urlpatterns = [
    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    
]

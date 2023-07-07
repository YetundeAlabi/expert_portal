"""
URL configuration for expert_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from tribe.views import RegionCreateAPIView, OfficeAddressCreateAPIView, OfficeAddressDestroyAPIView, OfficeAddressUpdateAPIView, OfficeAddressListAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls", namespace="accounts")),
    path("api/", include("staff_mgt.urls", namespace="staff_mgt")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    path("region/create/", RegionCreateAPIView.as_view(), name="create_region"),
    path("offices/create/", OfficeAddressCreateAPIView.as_view(), name="create_region"),
    path("offices/", OfficeAddressListAPIView.as_view(), name="list_offices"),
    path("offices/<int:pk>/update", OfficeAddressUpdateAPIView.as_view(), name="update_office_address"),
    path("offices/<int:pk>/delete", OfficeAddressDestroyAPIView.as_view(), name="delete_office_address"),

]

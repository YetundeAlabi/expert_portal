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
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from tribe.views import RegionCreateAPIView, LocationCreateAPIView, LocationDestroyAPIView, LocationUpdateAPIView, LocationListAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("accounts.urls", namespace="accounts")),
    path("api/", include("staff_mgt.urls", namespace="staff_mgt")),
    path("tribe/", include("tribe.urls", namespace="tribe")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("", SpectacularSwaggerView.as_view(url_name="schema")),
    path("region/create/", RegionCreateAPIView.as_view(), name="create_region"),
    path("offices/create/", LocationCreateAPIView.as_view(), name="create_region"),
    path("offices/", LocationListAPIView.as_view(), name="list_offices"),
    path("offices/<int:pk>/update", LocationUpdateAPIView.as_view(), name="location_update"),
    path("offices/<int:pk>/delete", LocationDestroyAPIView.as_view(), name="delete_location"),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

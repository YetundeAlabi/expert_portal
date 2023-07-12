from django.urls import path

from offices import views

app_name = "offices"

urlpatterns = [
    # path("countries", views.CountryListAPIView.as_view(), name="countries"),
    path("address/<int:country_pk>/city-address", views.OfficeAddressCreateAPIView.as_view(), name="office_address"),
    path("address/", views.OfficeAddressListAPIView.as_view(), name="address_list"),
    path("<int:pk>/update", views.OfficeAddressUpdateAPIView.as_view(), name="location_update"),
    path("<int:pk>/delete", views.OfficeAddressDestroyAPIView.as_view(), name="delete_location"),
]
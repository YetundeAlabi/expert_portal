from django.urls import path

from offices import views

app_name = "offices"

urlpatterns = [
    path("office/countries", views.CountryListAPIView.as_view(), name="countries"),
    path("office/countries/<int:country_pk>/cities", views.CityListCreateAPIView.as_view(), name="cities"),
    path("offices/create/", views.LocationListCreateAPIView.as_view(), name="list_create_location"),
    path("offices/<int:pk>/update", views.LocationUpdateAPIView.as_view(), name="location_update"),
    path("offices/<int:pk>/delete", views.LocationDestroyAPIView.as_view(), name="delete_location"),
]
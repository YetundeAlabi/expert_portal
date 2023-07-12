from django.urls import path

from offices import views

app_name = "offices"

urlpatterns = [
    path("countries", views.CountryListAPIView.as_view(), name="countries"),
    path("countries/<int:country_pk>/cities", views.CityListCreateAPIView.as_view(), name="cities"),
    path("countries/create", views.LocationListCreateAPIView.as_view(), name="list_create_location"),
    path("<int:pk>/update", views.LocationUpdateAPIView.as_view(), name="location_update"),
    path("<int:pk>/delete", views.LocationDestroyAPIView.as_view(), name="delete_location"),
]
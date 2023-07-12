from django.urls import path

from tribe import views

app_name = "tribe"
urlpatterns = [
    path("create", views.TribeCreateAPIView.as_view(), name="create_tribe"),
    path("", views.TribeListAPIView.as_view(), name="tribe_list"),
    path("<int:pk>/", views.TribeDetailUpdateAPIView.as_view(), name="tribe_detail_update"),
    # path("<int:pk>/update", views.TribeUpdateAPIView.as_view(), name="tribe_update"),
    path("<int:tribe_pk>/squads/<int:pk>/", views.SquadDetailUpdateAPIView.as_view(), name="squad_detail_update"),
    path("<int:tribe_pk>/squads", views.SquadListCreateAPIView.as_view(), name="squad_list_create"),
    path("<int:tribe_pk>/squads/export", views.ExportSquadAPIView.as_view(), name="export_squad"),
    # path("countries", views.CountryListAPIView.as_view(), name="countries"),
    path("address/<int:country_pk>/city-address", views.OfficeAddressCreateAPIView.as_view(), name="office_address"),
    path("address/", views.OfficeAddressListAPIView.as_view(), name="address_list"),
    path("address/<int:pk>/update", views.OfficeAddressUpdateAPIView.as_view(), name="location_update"),
    path("address/<int:pk>/delete", views.OfficeAddressDestroyAPIView.as_view(), name="delete_location"),
]
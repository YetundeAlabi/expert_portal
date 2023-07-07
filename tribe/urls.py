from django.urls import path

from tribe import views

app_name = "tribe"
urlpatterns = [
    path("create/", views.TribeCreateAPIView.as_view(), name="create_tribe"),
    path("", views.TribeListAPIView.as_view(), name="tribe_list"),
    path("<int:pk>/", views.TribeDetailUpdateAPIView.as_view(), name="tribe_detail_update"),
    # path("<int:pk>/update", views.TribeUpdateAPIView.as_view(), name="tribe_update"),
    path("<int:tribe_pk>/squads/<int:pk>/", views.SquadDetailUpdateAPIView.as_view(), name="squad_detail_update"),
    path("<int:tribe_pk>/squads", views.SquadListAPIView.as_view(), name="squad_list"),
    
]

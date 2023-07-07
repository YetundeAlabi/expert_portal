from django.urls import path

from tribe import views

app_name = "tribe"
urlpatterns = [
    path("create/", views.TribeCreateAPIView.as_view(), name="create_tribe"),
    path("", views.TribeListAPIView.as_view(), name="tribe_list"),
    path("<int:pk>/", views.TribeDetailAPIView.as_view(), name="tribe_detail"),
    path("<int:pk>/update", views.TribeUpdateAPIView.as_view(), name="tribe_update"),
    path("<int:tribe_pk>/squads/<int:pk>/", views.SquadDetailAPIView.as_view(), name="squad_detail"),
    path("<int:tribe_pk>/squads/<int:pk>/update", views.SquadUpdateAPIView.as_view(), name="squad_update"),
    
]

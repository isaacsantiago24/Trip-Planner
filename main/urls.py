from django.urls import path

from . import views

urlpatterns= [
    path('', views.display_login_and_register_page), #renders main page with an empty ''
    path('create', views.create_user), #once the register button is clicked, the create_user method is called
    path('login', views.login),

    path("logout", views.logout),
    
    path('dashboard', views.display_dashboard_page),

    path("trips/new", views.create_trip_page),
    path("trip/create", views.create_trip_action),

    path("trips/edit/<int:trip_id>", views.edit_trip_page),
    path("trips/edit/<int:trip_id>/update", views.edit_trip_action),




    path("trips/<int:trip_id>", views.view_trip_page),
    path("trips/<int:trip_id>/destroy", views.delete),


]
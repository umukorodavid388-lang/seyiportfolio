from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("services-details/<int:services_id>/", views.services_details, name="services_details"),
]
 

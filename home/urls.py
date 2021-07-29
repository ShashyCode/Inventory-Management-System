from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name ='home'),
    path("locations", views.location, name ='location'),
    path("movings", views.moving, name ='moving'),
    path("home", views.index, name ='home'),
    path("add_location", views.add_location, name = 'add_location'),
    path("add_product", views.add_product, name = 'add_product'),
    path("movement", views.movement, name ='movement'),
    path("edit_location/<int:pk>", views.editlocation, name ='editlocation'),
    path("edit_product/<int:pk>", views.editproduct, name ='editproduct'),
    path("locations/<int:pk>", views.deletelocation, name ='deletelocation'),
    path("home/<int:pk>", views.deleteproduct, name ='deleteproduct'),
    path("movement/<int:pk>", views.deletemovement, name ='deletemovement')
]
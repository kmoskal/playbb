from django.urls import path

from . import views

app_name = "magazyn"

urlpatterns = [
    path('', views.simple_upload, name='magazyn-home')
]

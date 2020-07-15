from django.urls import path

from . import views

app_name = "magazyn"

urlpatterns = [
    path('', views.simple_upload, name='magazyn-home'),
    path('lista-akcesorii', views.ListaAkcesoriView.as_view(), name='lista-akcesorii'),
    path('wyszukane-akcesoria', views.WyszukaneAkcesoriaView.as_view(), name='wyszukane-akcesoria'),
]

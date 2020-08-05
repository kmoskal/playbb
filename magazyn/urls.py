from django.urls import path

from . import views

app_name = "magazyn"

urlpatterns = [
    path('', views.upload_file_to_raport, name='magazyn-home'),
    path('wczytaj-stany', views.upload_file_to_magazyn, name='wczytaj-stany'),
    path('lista-akcesorii', views.ListaAkcesoriView.as_view(), name='lista-akcesorii'),
    path('wyszukane-akcesoria', views.WyszukaneAkcesoriaView.as_view(), name='wyszukane-akcesoria'),
]

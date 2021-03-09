from django.urls import path
from . import views

app_name = 'inwentaryzacja'

urlpatterns = [
    path('dodaj', views.RaportCreateView.as_view(), name='inwentaryzacja-dodaj'),
    path('', views.RaportListView.as_view(), name='inwentaryzacja-lista'),
    path('ostatni', views.RaportLastListView.as_view(), name='inwentaryzacja-ostatni'),
    path('detail/<int:pk>/', views.RaportDetailView.as_view(), name='inwentaryzacja-detail'),
    path('update/<int:pk>/', views.RaportUpdateView.as_view(), name='inwentaryzacja-update')
]

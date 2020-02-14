from django.urls import path
from . import views

app_name = 'akcesoria'

urlpatterns = [
    path('dodaj', views.AkcesoriaCreateView.as_view(), name='akcesoria-dodaj'),
    path('', views.AkcesoriaListView.as_view(), name='akcesoria-lista'),
    path('detail/<int:pk>', views.AkcesoriaDetailView.as_view(), name='akcesoria-detail'),
    path('update/<int:pk>/', views.AkcesoriaUpdateView.as_view(), name='akcesoria-update'),
    path('delete/<int:pk>/', views.AkcesoriaDeleteView.as_view(), name='akcesoria-delete'),
]

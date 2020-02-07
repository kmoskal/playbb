from django.urls import path
from . import views

app_name = 'akcesoria'

urlpatterns = [
    path('dodaj', views.AkcesoriaCreateView.as_view(), name='akcesoria-dodaj'),
    path('', views.AkcesoriaListView.as_view(), name='akcesoria-lista'),
    path('detail/', views.AkcesoriaDetailView.as_view(), name='akcesoria-detail')
    #path('', views.TemplateView.as_view(template_name='dashboard/dashboard_home.html'), name='dashboard_home'),
    #path('akcesoria')
]

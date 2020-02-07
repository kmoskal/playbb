from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.TemplateView.as_view(template_name='dashboard/dashboard_home.html'), name='dashboard_home'),
    #path('akcesoria')
]

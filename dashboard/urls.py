from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard-home'),
    #path('akcesoria')
]

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:account-login'
    template_name = 'dashboard/dashboard_home.html'

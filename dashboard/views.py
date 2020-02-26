from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import pandas as pd
from django_pandas.io import read_frame
from akcesoria.models import Akcesoria



class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:account-login'
    template_name = 'dashboard/dashboard_home.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        this_month = datetime.datetime.now().month
        queryset = Akcesoria.objects.filter(data__month=this_month)
        df = read_frame(queryset)
        kto_grp = df.groupby(['kto'])
        wartosc = kto_grp['kwota'].sum()
        slownik = wartosc.sort_values(ascending=False).to_dict()
        context['akcesoria'] = slownik
        context['suma'] = df['kwota'].sum()
        return context

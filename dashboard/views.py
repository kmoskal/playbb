from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime
import pandas as pd
from django_pandas.io import read_frame
from akcesoria.models import Akcesoria
from inwentaryzacja.models import Raport



class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:account-login'
    template_name = 'dashboard/dashboard_home.html'



    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        # context do akcesorii
        this_month = datetime.datetime.now().month
        queryset = Akcesoria.objects.filter(data__month=this_month)
        df = read_frame(queryset)
        kto_grp = df.groupby(['kto'])
        wartosc = kto_grp['kwota'].sum()
        slownik = wartosc.sort_values(ascending=False).to_dict()
        context['akcesoria'] = slownik
        context['suma'] = df['kwota'].sum()

        # context do inwentaryzacji
        def check_difference(x, y):
            if x is not None and y is not None:
                if y-x > 0:
                    return y-x
                elif y-x < 0:
                    return y-x
                else:
                    return "OK"
            else:
                return "Brak danych"

        qs = Raport.objects.last()
        if qs:
            context['telefony'] = check_difference(qs.telefony_elza, qs.telefony_stan)
            context['voice'] = check_difference(qs.voice_elza, qs.voice_stan)
            context['starter_data'] = check_difference(qs.data_elza, qs.data_stan)
            context['zdrapki'] = check_difference(qs.zdrapki_elza, qs.zdrapki_stan)
            context['doladowania'] = check_difference(qs.doladowania_elza, qs.doladowania_stan)
            context['gotowka'] = check_difference(qs.kasa_elza, qs.kasa_stan)
            context['data'] = qs.data_raportu
            context['uzyczenie'] = qs.uzyczenie_elza
            context['folie'] = qs.folia_elza
            context['raport_id'] = qs.id

        return context

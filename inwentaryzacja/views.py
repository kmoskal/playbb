from django.shortcuts import render
from django.views.generic import (
        TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
    )
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
import datetime

from .models import Raport

class RaportView(LoginRequiredMixin, TemplateView):
    pass

class RaportCreateView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:account-login'
    model = Raport
    fields = (
        'telefony_elza', 'telefony_stan', 'voice_elza', 'voice_stan',
        'data_elza', 'data_stan', 'zdrapki_elza', 'zdrapki_stan',
        'doladowania_elza', 'doladowania_stan', 'kasa_elza', 'kasa_stan'
    )

    def form_valid(self, form):
        form.instance.kto = self.request.user
        return super().form_valid(form)

class RaportUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'accounts:account-login'
    model = Raport
    fields = (
        'telefony_elza', 'telefony_stan', 'voice_elza', 'voice_stan',
        'data_elza', 'data_stan', 'zdrapki_elza', 'zdrapki_stan',
        'doladowania_elza', 'doladowania_stan', 'kasa_elza', 'kasa_stan'
    )

    def form_valid(self, form):
        form.instance.kto = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("inwentaryzacja:inwentaryzacja-lista")



class RaportListView(LoginRequiredMixin, ListView):
    login_url ='accounts:account-login'
    this_month = datetime.datetime.now().month
    dzis = datetime.datetime.now().today
    queryset = Raport.objects.filter(data_raportu__month=this_month)
    model = Raport
    context_object_name = 'raporty'
    ordering = ['-data_raportu']

    # def get_context_data(self, **kwargs):
    #     context = super(RaportListView, self).get_context_data(**kwargs)
    #     this_month = datetime.datetime.now().month
    #     dzis = datetime.datetime.now().today
    #     queryset = Raport.objects.filter(data_raportu__month=this_month)
    #     ordering = ['-data_raportu']
    #     context['qs'] = queryset
    #     context['data'] = self.dzis
    #     return context

class RaportLastListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:account-login'
    template_name = 'inwentaryzacja/raport_last_list.html'
    queryset = Raport.objects.latest('data_raportu')
    model = Raport
    context_object_name = 'raporty'



class RaportDetailView(LoginRequiredMixin, DetailView):
    login_url='accounts:acount-login'
    model = Raport

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        dzis = datetime.datetime.now().today()
        context['dzis'] = dzis
        return context

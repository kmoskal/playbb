from django.shortcuts import render, redirect
from django.http import Http404
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        this_month = datetime.datetime.now().month
        context["raporty"] = self.model.objects.filter(data_raportu__month=this_month).order_by('-data_raportu', '-pk')
        return context


class RaportUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'accounts:account-login'
    template_name = 'inwentaryzacja/raport_update.html'
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
        return reverse("dashboard:dashboard-home")

class RaportListView(LoginRequiredMixin, ListView):
    login_url ='accounts:account-login'
    this_month = datetime.datetime.now().month
    dzis = datetime.datetime.now().today
    queryset = Raport.objects.filter(data_raportu__month=this_month)
    model = Raport
    context_object_name = 'raporty'
    ordering = ['-data_raportu', '-pk']

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
    #this_month = datetime.datetime.now().month
    #queryset = Raport.objects.filter(data_raportu__month=this_month).last()
    model = Raport
    context_object_name = 'raporty'
    queryset = Raport.objects.all().last()






class RaportDetailView(LoginRequiredMixin, DetailView):
    login_url='accounts:account-login'
    model = Raport
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     dzis = datetime.datetime.now().today()
    #     context['dzis'] = dzis
    #     return context
    #<td><a href="{% url 'inwentaryzacja:inwentaryzacja-update' pk=raport.id %}"><i class="fas fa-edit"></i></a></td>

    def get_context_data(self, **kwargs):
        context = super(RaportDetailView, self).get_context_data(**kwargs)
        context['raport'] = Raport.objects.get(pk=self.kwargs['pk'])


        def check_difference(x, y):
            if x and y:
                if y-x > 0:
                    return y-x
                elif y-x < 0:
                    return y-x
                else:
                    return "OK"
            else:
                return "Brak danych"

        qs = Raport.objects.get(pk=self.kwargs['pk'])
        context['telefony'] = check_difference(qs.telefony_elza, qs.telefony_stan)
        context['voice'] = check_difference(qs.voice_elza, qs.voice_stan)
        context['starter_data'] = check_difference(qs.data_elza, qs.data_stan)
        context['zdrapki'] = check_difference(qs.zdrapki_elza, qs.zdrapki_stan)
        context['doladowania'] = check_difference(qs.doladowania_elza, qs.doladowania_stan)
        context['gotowka'] = check_difference(qs.kasa_elza, qs.kasa_stan)
        context['data'] = qs.data_raportu

        return context

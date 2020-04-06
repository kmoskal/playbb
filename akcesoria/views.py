from django.views.generic import TemplateView
from django.views.generic import (
        CreateView, ListView, DetailView, UpdateView, DeleteView
    )
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core import serializers
import datetime
import pandas as pd
from django_pandas.io import read_frame
from .models import Akcesoria
import json



class AkcesoriaListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:account-login'
    this_month = datetime.datetime.now().month
    queryset = Akcesoria.objects.filter(data__month=this_month).order_by('-data', '-pk')
    model = Akcesoria
    context_object_name = 'akcesoria'

class AkcesoriaCreateView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:account-login'
    fields = ('co', 'kwota', 'model')
    model = Akcesoria

    def form_valid(self, form):
        form.instance.kto = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        this_month = datetime.datetime.now().month
        context["akcesoria"] = self.model.objects.filter(data__month=this_month).order_by('-data', '-pk')
        return context

class AkcesoriaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = 'accounts:account-login'
    template_name = 'akcesoria/akcesoria_update.html'
    fields = ('co', 'kwota', 'model')
    model = Akcesoria

    def form_valid(self, form):
        form.instance.kto = self.request.user
        return super().form_valid(form)

    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.kto:
            return True
        return False

    def get_success_url(self):
        return reverse("akcesoria:akcesoria-lista")


class AkcesoriaDetailView(LoginRequiredMixin, DetailView):
    login_url = 'accounts:account-login'
    model = Akcesoria


class AkcesoriaDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = 'accounts:account-login'
    model = Akcesoria


    def test_func(self):
        obj = self.get_object()
        if self.request.user == obj.kto:
            return True
        return False

    def get_success_url(self):
        return reverse("akcesoria:akcesoria-lista")


class AkcesoriaMonthView(LoginRequiredMixin, TemplateView):
    login_url = 'accounts:account-login'
    template_name = 'akcesoria/akcesoria_month.html'



    def get_context_data(self, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        context = super(AkcesoriaMonthView, self).get_context_data(**kwargs)
        queryset = Akcesoria.objects.filter(data__month=month, data__year=year)
        df = read_frame(queryset)
        kto_grp = df.groupby(['kto'])
        wartosc = kto_grp['kwota'].sum()
        slownik = wartosc.sort_values(ascending=False).to_dict()
        context['akcesoria'] = slownik
        context['akcesoria_json'] = wartosc.sort_values(ascending=False).to_json()
        context['suma'] = df['kwota'].sum()
        data = {
            "rok": year,
            "miesiac": month,
        }
        context['data'] = data
        return context

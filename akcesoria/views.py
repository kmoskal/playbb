from django.views.generic import TemplateView
from django.views.generic import (
        CreateView, ListView, DetailView, UpdateView, DeleteView
    )
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import datetime

from .models import Akcesoria



class AkcesoriaListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:account-login'
    template_name = 'akcesoria/lista.html'
    this_month = datetime.datetime.now().month
    queryset = Akcesoria.objects.filter(data__month=this_month)
    #queryset = Akcesoria.objects.all()
    model = Akcesoria
    context_object_name = 'akcesoria'
    ordering = ['-data']

class AkcesoriaCreateView(LoginRequiredMixin, CreateView):
    login_url = 'accounts:account-login'
    fields = ('co', 'kwota', 'model')
    model = Akcesoria

    def form_valid(self, form):
        form.instance.kto = self.request.user
        return super().form_valid(form)

class AkcesoriaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = 'accounts:account-login'
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

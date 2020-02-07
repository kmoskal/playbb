from django.views.generic import TemplateView
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Akcesoria



class AkcesoriaListView(LoginRequiredMixin, TemplateView):
    template_name = 'akcesoria/lista.html'

class AkcesoriaCreateView(LoginRequiredMixin, CreateView):
    template_name = 'akcesoria/akcesoria_dodaj.html'
    fields = ('kto', 'co', 'kwota', 'model')
    model = Akcesoria

class AkcesoriaDetailView(DetailView):
    context_object_name = 'Akcesoria'
    queryset = Akcesoria.objects.all()

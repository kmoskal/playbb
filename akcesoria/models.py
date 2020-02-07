from django.db import models
from django.conf import settings
from django.urls import reverse
from model_utils import Choices
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
# Create your models here.

class Akcesoria(models.Model):

    CO_CHOICES = Choices(
        ('plecki', _('Plecki')),
        ('book', _('Książka')),
        ('szklo', _('Szkło')),
        ('folia', _('Folia')),
        ('inne', _('Inne')),
    )

    data    = models.DateField(auto_now_add=True)
    kto     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=User)
    co      = models.CharField(max_length=15, choices=CO_CHOICES, default=CO_CHOICES.plecki)
    kwota   = models.DecimalField(max_digits=5, decimal_places=2)
    model   = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return self.co

    def get_absolute_url(self):
        return reverse("dashboard:dashboard_home")

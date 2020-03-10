from django.db import models
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Raport(models.Model):
    data_raportu = models.DateField(auto_now_add=True)
    kto = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=User)
    telefony_elza = models.IntegerField()
    telefony_stan = models.IntegerField()
    voice_elza = models.IntegerField()
    voice_stan = models.IntegerField()
    data_elza = models.IntegerField()
    data_stan = models.IntegerField()
    zdrapki_elza = models.IntegerField()
    zdrapki_stan = models.IntegerField()
    doladowania_elza = models.IntegerField()
    doladowania_stan = models.IntegerField()
    kasa_elza = models.DecimalField(max_digits=7, decimal_places=2)
    kasa_stan = models.DecimalField(max_digits=7, decimal_places=2)


    def __str__(self):
        return self.kto

    def get_absolute_url(self):
        return reverse("inwentaryzacja:inwentaryzacja-lista")

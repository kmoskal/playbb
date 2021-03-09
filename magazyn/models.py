from django.db import models


class StanAkcesoria(models.Model):
    symbol = models.CharField(max_length=50)
    nazwa = models.CharField(max_length=250)
    cena = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    ilosc = models.PositiveSmallIntegerField()
    searchstring = models.CharField(max_length=250, default="Null")

    def __str__(self):
        return str(self.nazwa)

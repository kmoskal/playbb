from django.db import models

class StanAkcesoria(models.Model):
    symbol = models.CharField(max_length=15)
    nazwa = models.CharField(max_length=150)
    ilosc = models.PositiveSmallIntegerField()
    searchstring = models.CharField(max_length=150, default="Null")


    def __str__(self):
        return str(self.nazwa)

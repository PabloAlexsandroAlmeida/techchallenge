from datetime import date

from django.db import models


class AnoProducao(models.Model):
    ano = models.DateField()
    quantidade = models.IntegerField()

class Producao(models.Model):
    control = models.CharField(max_length=100, default=False, blank=False)
    produto =  models.CharField(max_length=255, default=False, blank=False)
    ano = models.ManyToManyField(AnoProducao)

    def __str__(self):
        return self.control

from datetime import date

from django.db import models

class AnoProducao(models.Model):
    ano = models.IntegerField()
    quantidade = models.BigIntegerField()

    def __str__(self):
        return f"{self.ano}: {self.quantidade}"

class Producao(models.Model):
    produto = models.CharField(max_length=255, blank=False)
    tipo = models.CharField(max_length=255, blank=False)
    anos = models.ManyToManyField(AnoProducao)

    def __str__(self):
        return f"{self.produto} ({self.tipo})"

class Comercio(models.Model):
    produto = models.CharField(max_length=255, blank=False)
    tipo = models.CharField(max_length=255, blank=False)
    anos = models.ManyToManyField(AnoProducao)

    def __str__(self):
        return f"{self.produto} ({self.tipo})"
    
class Processamento(models.Model):
    cultivo = models.CharField(max_length=255, blank=False)
    tipo = models.CharField(max_length=255, blank=False)
    anos = models.ManyToManyField(AnoProducao)

    def __str__(self):
        return f"{self.cultivo} ({self.tipo})"
    
class Exportacao(models.Model):
    pais = models.CharField(max_length=100)
    ano_producao = models.ForeignKey(AnoProducao, on_delete=models.CASCADE, related_name="exportacoes")
    valor_usd = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"Exportação {self.pais} - {self.ano_producao.ano}: {self.valor_usd} USD"
    
class Importacao(models.Model):
    pais = models.CharField(max_length=100)
    ano_producao = models.ForeignKey(AnoProducao, on_delete=models.CASCADE, related_name="importacoes")
    valor_usd = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"Importação {self.pais} - {self.ano_producao.ano}: {self.valor_usd} USD"

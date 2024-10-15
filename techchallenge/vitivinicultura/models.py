from django.db import models

class BaseModel(models.Model):
    class Meta:
        abstract = True

class ProdutoTipoModel(BaseModel):
    produto = models.CharField(max_length=100, default='produto_desconhecido')
    tipo = models.CharField(max_length=100, default='tipo_desconhecido')

    class Meta:
        abstract = True

class Producao(ProdutoTipoModel):
    # outros campos

    def __str__(self):
        return f"Produção - {self.produto} ({self.tipo})"

class Comercio(ProdutoTipoModel):
    # outros campos

    def __str__(self):
        return f"Comércio - {self.produto} ({self.tipo})"

class Processamento(ProdutoTipoModel):
    # outros campos

    def __str__(self):
        return f"Processamento - {self.produto} ({self.tipo})"

class Pais(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Importacao(models.Model):
    pais = models.CharField(max_length=100)

    def __str__(self):
        return f"Importação de {self.pais}"

class Exportacao(models.Model):
    pais = models.CharField(max_length=100)

    def __str__(self):
        return f"Exportação para {self.pais}"

# Modelo de AnoValor para armazenar os valores por ano de cada tipo
class AnoValor(models.Model):
    producao = models.ForeignKey(Producao, null=True, blank=True, on_delete=models.CASCADE)
    comercio = models.ForeignKey(Comercio, null=True, blank=True, on_delete=models.CASCADE)
    processamento = models.ForeignKey(Processamento, null=True, blank=True, on_delete=models.CASCADE)
    exportacao = models.ForeignKey(Exportacao, null=True, blank=True, on_delete=models.CASCADE)
    importacao = models.ForeignKey(Importacao, null=True, blank=True, on_delete=models.CASCADE)
    ano = models.IntegerField(default=1970)  # Definindo 1970 como valor padrão
    valor = models.FloatField(default=0.0)
    tipo_valor = models.CharField(max_length=50, default='valor')

    def __str__(self):
        return f"{self.ano}: {self.valor}"

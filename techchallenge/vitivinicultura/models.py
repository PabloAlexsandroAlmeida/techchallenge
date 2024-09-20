from django.db import models

# Modelo abstrato que será herdado pelos outros modelos
class BaseModel(models.Model):
    produto = models.CharField(max_length=100, default='produto_desconhecido')
    tipo = models.CharField(max_length=100, default='tipo_desconhecido')

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.produto} ({self.tipo})"

# Modelo de Produção
class Producao(BaseModel):
    pass

# Modelo de Comércio
class Comercio(BaseModel):
    pass

# Modelo de Processamento
class Processamento(BaseModel):
    pass

# Modelo de Exportação
class Exportacao(BaseModel):
    pass

# Modelo de Importação
class Importacao(BaseModel):
    pass

# Modelo de AnoValor para armazenar os valores por ano de cada tipo
class AnoValor(models.Model):
    producao = models.ForeignKey(Producao, null=True, blank=True, on_delete=models.CASCADE)
    comercio = models.ForeignKey(Comercio, null=True, blank=True, on_delete=models.CASCADE)
    processamento = models.ForeignKey(Processamento, null=True, blank=True, on_delete=models.CASCADE)
    exportacao = models.ForeignKey(Exportacao, null=True, blank=True, on_delete=models.CASCADE)
    importacao = models.ForeignKey(Importacao, null=True, blank=True, on_delete=models.CASCADE)
    ano = models.IntegerField(default=1970)  # Definindo 1970 como valor padrão
    valor = models.BigIntegerField(default=0)  # Usando 0 como valor padrão

    def __str__(self):
        return f"{self.ano}: {self.valor}"

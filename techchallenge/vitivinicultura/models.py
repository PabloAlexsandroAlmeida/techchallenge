from django.db import models

class BaseModel(models.Model):
    """
    Modelo base abstrato para fornecer funcionalidades comuns a outros modelos.
    """
    class Meta:
        abstract = True


class Produto(models.Model):
    """
    Modelo que representa um produto e seu tipo.
    """
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)

    class Meta:
        unique_together = ('nome', 'tipo')
        verbose_name_plural = "Produtos"

    def __str__(self):
        return f"{self.nome} - {self.tipo}"


class Pais(models.Model):
    """
    Modelo que representa um país.
    """
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome


class Ano(models.Model):
    """
    Modelo que representa um ano específico.
    """
    ano = models.IntegerField(unique=True)

    def __str__(self):
        return str(self.ano)


class Producao(models.Model):
    """
    Modelo que representa os dados de produção.
    """
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="producoes")
    ano = models.ForeignKey(Ano, on_delete=models.CASCADE, related_name="producoes", default=2020)  
    quantidade = models.FloatField(default=0.0)  

    def __str__(self):
        return f"Produção de {self.produto} em {self.ano}"


class Comercializacao(models.Model):
    """
    Modelo que representa os dados de comercialização.
    """
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="comercializacoes")
    ano = models.ForeignKey(Ano, on_delete=models.CASCADE, related_name="comercializacoes", default=2020)  
    quantidade = models.FloatField(default=0.0)  

    def __str__(self):
        return f"Comercialização de {self.produto} em {self.ano}"


class Processamento(models.Model):
    """
    Modelo que representa os dados de processamento.
    """
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="processamentos")
    ano = models.ForeignKey(Ano, on_delete=models.CASCADE, related_name="processamentos", default=2020)  
    quantidade = models.FloatField(default=0.0)  

    def __str__(self):
        return f"Processamento de {self.produto} em {self.ano}"


class Importacao(models.Model):
    """
    Modelo que representa os dados de importação.
    """
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name="importacoes")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="importacoes")
    ano = models.ForeignKey(Ano, on_delete=models.CASCADE, related_name="importacoes", default=2020)  
    quantidade = models.FloatField(default=0.0)  
    valor = models.FloatField(default=0.0)  

    def __str__(self):
        return f"Importação de {self.produto} de {self.pais} em {self.ano}"


class Exportacao(models.Model):
    """
    Modelo que representa os dados de exportação.
    """
    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name="exportacoes")
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE, related_name="exportacoes")
    ano = models.ForeignKey(Ano, on_delete=models.CASCADE, related_name="exportacoes", default=2020)  
    quantidade = models.FloatField(default=0.0)  
    valor = models.FloatField(default=0.0)  

    def __str__(self):
        return f"Exportação de {self.produto} para {self.pais} em {self.ano}"

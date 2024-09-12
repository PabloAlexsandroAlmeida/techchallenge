from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class ProdutoBase(models.Model):
    """
    Modelo base abstrato para produtos com campos comuns.
    """
    nome = models.CharField(max_length=255)
    tipo = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.nome} ({self.tipo})"


class Producao(ProdutoBase):
    """
    Modelo que representa um produto de produção agrícola.
    """
    pass


class ProducaoDados(models.Model):
    """
    Modelo para armazenar dados de produção por ano.
    """
    producao = models.ForeignKey(Producao, on_delete=models.CASCADE, related_name='dados')
    ano = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    quantidade = models.BigIntegerField()

    class Meta:
        unique_together = ('producao', 'ano')
        ordering = ['ano']

    def __str__(self):
        return f"{self.producao} - {self.ano}: {self.quantidade}"


class Comercio(ProdutoBase):
    """
    Modelo que representa um produto de comércio.
    """
    pass


class ComercioDados(models.Model):
    """
    Modelo para armazenar dados de comércio por ano.
    """
    comercio = models.ForeignKey(Comercio, on_delete=models.CASCADE, related_name='dados')
    ano = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    quantidade = models.BigIntegerField()

    class Meta:
        unique_together = ('comercio', 'ano')
        ordering = ['ano']

    def __str__(self):
        return f"{self.comercio} - {self.ano}: {self.quantidade}"


class Processamento(ProdutoBase):
    """
    Modelo que representa um cultivo processado.
    """
    pass


class ProcessamentoDados(models.Model):
    """
    Modelo para armazenar dados de processamento por ano.
    """
    processamento = models.ForeignKey(Processamento, on_delete=models.CASCADE, related_name='dados')
    ano = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    quantidade = models.BigIntegerField()

    class Meta:
        unique_together = ('processamento', 'ano')
        ordering = ['ano']

    def __str__(self):
        return f"{self.processamento} - {self.ano}: {self.quantidade}"


class TransacaoBase(models.Model):
    """
    Modelo base abstrato para transações de importação e exportação.
    """
    pais = models.CharField(max_length=100)
    ano = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    quantidade = models.BigIntegerField(null=True, blank=True)
    valor_usd = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        abstract = True
        ordering = ['ano']

    def __str__(self):
        return f"{self.pais} - {self.ano}: {self.valor_usd} USD"


class Exportacao(TransacaoBase):
    """
    Modelo que representa dados de exportação.
    """

    class Meta:
        verbose_name_plural = 'Exportações'

    def __str__(self):
        return f"Exportação {super().__str__()}"


class Importacao(TransacaoBase):
    """
    Modelo que representa dados de importação.
    """

    class Meta:
        verbose_name_plural = 'Importações'

    def __str__(self):
        return f"Importação {super().__str__()}"

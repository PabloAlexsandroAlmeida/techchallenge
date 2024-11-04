from django.db import models


class BaseModel(models.Model):
    """
    Modelo base abstrato para fornecer funcionalidades comuns a outros modelos.

    Este modelo não será criado no banco de dados, mas servirá como base
    para outros modelos que herdam dele.
    """

    class Meta:
        abstract = True


class ProdutoTipoModel(BaseModel):
    """
    Modelo abstrato que inclui os campos 'produto' e 'tipo'.

    Este modelo é destinado a ser herdado por outros modelos que compartilham
    esses campos, evitando duplicação de código.
    """

    produto = models.CharField(max_length=100, default="produto_desconhecido")
    tipo = models.CharField(max_length=100, default="tipo_desconhecido")

    class Meta:
        abstract = True


class Producao(ProdutoTipoModel):
    """
    Modelo que representa os dados de produção.

    Herda de ProdutoTipoModel e pode incluir campos adicionais específicos
    para a produção.
    """

    # Adicione outros campos específicos para Producao, se necessário

    def __str__(self) -> str:
        return f"Produção - {self.produto} ({self.tipo})"


class Comercio(ProdutoTipoModel):
    """
    Modelo que representa os dados de comércio.

    Herda de ProdutoTipoModel e pode incluir campos adicionais específicos
    para o comércio.
    """

    # Adicione outros campos específicos para Comercio, se necessário

    def __str__(self) -> str:
        return f"Comércio - {self.produto} ({self.tipo})"


class Processamento(ProdutoTipoModel):
    """
    Modelo que representa os dados de processamento.

    Herda de ProdutoTipoModel e pode incluir campos adicionais específicos
    para o processamento.
    """

    # Adicione outros campos específicos para Processamento, se necessário

    def __str__(self) -> str:
        return f"Processamento - {self.produto} ({self.tipo})"


class Pais(models.Model):
    """
    Modelo que representa um país.

    Este modelo é usado para relacionar países com importações e exportações.
    """

    nome = models.CharField(max_length=100, unique=True)

    def __str__(self) -> str:
        return self.nome


class Importacao(ProdutoTipoModel):
    """
    Modelo que representa os dados de importação.

    Relaciona-se com o modelo Pais através de uma chave estrangeira.
    """

    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name="importacoes")

    def __str__(self) -> str:
        return f"Importação - {self.produto} ({self.tipo}) de {self.pais.nome}"


class Exportacao(ProdutoTipoModel):
    """
    Modelo que representa os dados de exportação.

    Relaciona-se com o modelo Pais através de uma chave estrangeira.
    """

    pais = models.ForeignKey(Pais, on_delete=models.CASCADE, related_name="exportacoes")

    def __str__(self) -> str:
        return f"Exportação - {self.produto} ({self.tipo}) para {self.pais.nome}"


class AnoValor(models.Model):
    """
    Modelo para armazenar os valores por ano de cada tipo de dados.

    Este modelo permite registrar valores (como quantidade ou valor monetário)
    associados a um ano específico e relacionados a um dos modelos principais.
    """

    producao = models.ForeignKey(
        Producao,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="anos_valores",
    )
    comercio = models.ForeignKey(
        Comercio,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="anos_valores",
    )
    processamento = models.ForeignKey(
        Processamento,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="anos_valores",
    )
    exportacao = models.ForeignKey(
        Exportacao,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="anos_valores",
    )
    importacao = models.ForeignKey(
        Importacao,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="anos_valores",
    )
    ano = models.IntegerField()  # O ano deve ser explicitamente definido
    valor = models.FloatField(default=0.0)
    tipo_valor = models.CharField(max_length=50, default="valor")

    def __str__(self) -> str:
        return f"{self.ano}: {self.valor}"

    class Meta:
        verbose_name = "Ano e Valor"
        verbose_name_plural = "Anos e Valores"

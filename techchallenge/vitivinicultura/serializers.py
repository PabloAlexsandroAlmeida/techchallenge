from rest_framework import serializers
from .models import (
    Producao,
    Comercio,
    Processamento,
    Exportacao,
    Importacao,
    AnoValor,
    Pais,
)


# Serializer para o modelo AnoValor, que representa valores por ano associados aos modelos principais.
class AnoValorSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo AnoValor.

    Representa os valores associados a um ano específico.
    """

    class Meta:
        model = AnoValor
        fields = ["ano", "valor", "tipo_valor"]


# Serializer para o modelo Pais, utilizado em Importacao e Exportacao.
class PaisSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Pais.
    """

    class Meta:
        model = Pais
        fields = ["nome"]


# Serializer base para modelos que possuem 'produto' e 'tipo' como campos.
class ProdutoTipoSerializer(serializers.ModelSerializer):
    """
    Serializer base para modelos com campos 'produto' e 'tipo'.

    Inclui os valores associados a cada ano.
    """

    valores = AnoValorSerializer(source="anos_valores", many=True, read_only=True)

    class Meta:
        fields = ["produto", "tipo", "valores"]


# Serializer para Producao, incluindo valores por ano.
class ProducaoSerializer(ProdutoTipoSerializer):
    """
    Serializer para o modelo Producao.

    Herda de ProdutoTipoSerializer.
    """

    class Meta(ProdutoTipoSerializer.Meta):
        model = Producao


# Serializer para Comercio, incluindo valores por ano.
class ComercioSerializer(ProdutoTipoSerializer):
    """
    Serializer para o modelo Comercio.

    Herda de ProdutoTipoSerializer.
    """

    class Meta(ProdutoTipoSerializer.Meta):
        model = Comercio


# Serializer para Processamento, incluindo valores por ano.
class ProcessamentoSerializer(ProdutoTipoSerializer):
    """
    Serializer para o modelo Processamento.

    Herda de ProdutoTipoSerializer.
    """

    class Meta(ProdutoTipoSerializer.Meta):
        model = Processamento


# Serializer base para modelos que possuem o campo 'pais'.
class PaisRelatedSerializer(serializers.ModelSerializer):
    """
    Serializer base para modelos com campo 'pais'.

    Inclui os valores associados a cada ano.
    """

    pais = PaisSerializer(read_only=True)
    valores = AnoValorSerializer(source="anos_valores", many=True, read_only=True)

    class Meta:
        fields = ["pais", "valores"]


# Serializer para Exportacao, incluindo valores por ano.
class ExportacaoSerializer(PaisRelatedSerializer):
    """
    Serializer para o modelo Exportacao.

    Herda de PaisRelatedSerializer.
    """

    pais = PaisSerializer(read_only=True)

    class Meta(ProdutoTipoSerializer.Meta):
        model = Exportacao
        fields = ProdutoTipoSerializer.Meta.fields + ["pais"]


# Serializer para Importacao, incluindo valores por ano.
class ImportacaoSerializer(PaisRelatedSerializer):
    """
    Serializer para o modelo Importacao.

    Herda de PaisRelatedSerializer.
    """

    pais = PaisSerializer(read_only=True)
    
    class Meta(ProdutoTipoSerializer.Meta):
        model = Importacao
        fields = ProdutoTipoSerializer.Meta.fields + ["pais"]

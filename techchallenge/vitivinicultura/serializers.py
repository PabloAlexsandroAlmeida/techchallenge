from rest_framework import serializers
from .models import (
    Producao,
    Comercializacao, 
    Processamento,
    Exportacao,
    Importacao,
    Ano,
    Pais, 
)

class AnoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Ano.
    Representa os valores associados a um ano específico.
    """

    class Meta:
        model = Ano
        fields = ["ano"]

class PaisSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Pais.
    """

    class Meta:
        model = Pais
        fields = ["nome"]

class ProdutoTipoSerializer(serializers.ModelSerializer):
    """
    Serializer base para modelos com campos 'produto' e 'tipo'.
    Inclui os valores associados a cada ano.
    """

    class Meta:
        fields = ["produto", "tipo"]

class ProducaoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Producao.
    """
    produto = serializers.StringRelatedField()
    ano = serializers.StringRelatedField()

    class Meta:
        model = Producao
        fields = ["produto", "ano", "quantidade"]

class ComercializacaoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Comercializacao.
    """
    produto = serializers.StringRelatedField()
    ano = serializers.StringRelatedField()

    class Meta:
        model = Comercializacao
        fields = ["produto", "ano", "quantidade"]

class ProcessamentoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Processamento.
    """
    produto = serializers.StringRelatedField()
    ano = serializers.StringRelatedField()

    class Meta:
        model = Processamento
        fields = ["produto", "ano", "quantidade"]

class ExportacaoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Exportacao.
    Inclui o país e os valores por ano.
    """
    produto = serializers.StringRelatedField()
    ano = serializers.StringRelatedField()
    pais = PaisSerializer(read_only=True)

    class Meta:
        model = Exportacao
        fields = ["pais", "produto", "ano", "quantidade", "valor"]

class ImportacaoSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Importacao.
    Inclui o país e os valores por ano.
    """
    produto = serializers.StringRelatedField()
    ano = serializers.StringRelatedField()
    pais = PaisSerializer(read_only=True)

    class Meta:
        model = Importacao
        fields = ["pais", "produto", "ano", "quantidade", "valor"]

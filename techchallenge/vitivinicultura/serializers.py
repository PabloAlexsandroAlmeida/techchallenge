from rest_framework import serializers
from .models import Producao, Comercio, Processamento, Exportacao, Importacao, AnoValor

class AnoValorSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnoValor
        fields = ['ano', 'valor']

class ProducaoSerializer(serializers.ModelSerializer):
    valores = AnoValorSerializer(source='anovalor_set', many=True, read_only=True)

    class Meta:
        model = Producao
        fields = ['produto', 'tipo', 'valores']

class ComercioSerializer(serializers.ModelSerializer):
    valores = AnoValorSerializer(source='anovalor_set', many=True, read_only=True)

    class Meta:
        model = Comercio
        fields = ['produto', 'tipo', 'valores']

class ProcessamentoSerializer(serializers.ModelSerializer):
    valores = AnoValorSerializer(source='anovalor_set', many=True, read_only=True)

    class Meta:
        model = Processamento
        fields = ['produto', 'tipo', 'valores']

class ExportacaoSerializer(serializers.ModelSerializer):
    valores = AnoValorSerializer(source='anovalor_set', many=True, read_only=True)

    class Meta:
        model = Exportacao
        fields = ['produto', 'tipo', 'valores']

class ImportacaoSerializer(serializers.ModelSerializer):
    valores = AnoValorSerializer(source='anovalor_set', many=True, read_only=True)

    class Meta:
        model = Importacao
        fields = ['produto', 'tipo', 'valores']

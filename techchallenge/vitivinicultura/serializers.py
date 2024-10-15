from rest_framework import serializers
from .models import Producao, Comercio, Processamento, Exportacao, Importacao, AnoValor

# Definindo primeiro o AnoValorSerializer, pois será usado nos outros serializers
class AnoValorSerializer(serializers.ModelSerializer):
    producao = serializers.StringRelatedField(read_only=True)
    comercio = serializers.StringRelatedField(read_only=True)
    processamento = serializers.StringRelatedField(read_only=True)
    exportacao = serializers.StringRelatedField(read_only=True)
    importacao = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AnoValor
        fields = ['ano', 'valor', 'producao', 'comercio', 'processamento', 'exportacao', 'importacao']

# Agora, podemos definir o ProducaoSerializer, que depende do AnoValorSerializer
class ProducaoSerializer(serializers.ModelSerializer):
    valores = AnoValorSerializer(source='anovalor_set', many=True, read_only=True)

    class Meta:
        model = Producao
        fields = ['produto', 'tipo', 'valores']

# Da mesma forma, para os outros serializers
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
        fields = ['pais', 'valores']

class ImportacaoSerializer(serializers.ModelSerializer):
    valores = AnoValorSerializer(source='anovalor_set', many=True, read_only=True)

    class Meta:
        model = Importacao
        fields = ['pais', 'valores']

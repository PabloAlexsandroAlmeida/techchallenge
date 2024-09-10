from rest_framework import serializers
from .models import Producao, Comercio, Processamento, Exportacao, Importacao

class ProducaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producao
        fields = '__all__'

class ComercioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comercio
        fields = '__all__'

class ProcessamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processamento
        fields = '__all__'

class ExportacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exportacao
        fields = '__all__'

class ImportacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Importacao
        fields = '__all__'
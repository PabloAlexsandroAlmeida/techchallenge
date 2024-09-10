from rest_framework import viewsets
from .models import Producao, Comercio, Processamento, Exportacao, Importacao
from .serializers import ProducaoSerializer, ComercioSerializer, ProcessamentoSerializer, ExportacaoSerializer, ImportacaoSerializer

class ProducaoViewSet(viewsets.ModelViewSet):
    queryset = Producao.objects.all()
    serializer_class = ProducaoSerializer

class ComercioViewSet(viewsets.ModelViewSet):
    queryset = Comercio.objects.all()
    serializer_class = ComercioSerializer

class ProcessamentoViewSet(viewsets.ModelViewSet):
    queryset = Processamento.objects.all()
    serializer_class = ProcessamentoSerializer

class ExportacaoViewSet(viewsets.ModelViewSet):
    queryset = Exportacao.objects.all()
    serializer_class = ExportacaoSerializer

class ImportacaoViewSet(viewsets.ModelViewSet):
    queryset = Importacao.objects.all()
    serializer_class = ImportacaoSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Producao, Comercio, Processamento, Exportacao, Importacao, AnoValor
from .serializers import (
    ProducaoSerializer, ComercioSerializer, ProcessamentoSerializer,
    ExportacaoSerializer, ImportacaoSerializer, AnoValorSerializer
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Criação de uma classe base para evitar repetição de código
class BaseModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para modelos que herdam de BaseModel.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

# Definindo os ViewSets específicos para cada modelo

class ProducaoViewSet(BaseModelViewSet):
    queryset = Producao.objects.all()
    serializer_class = ProducaoSerializer
    filterset_fields = ['produto', 'tipo']  # Campos válidos para Producao
    search_fields = ['produto', 'tipo']
    ordering_fields = ['produto', 'tipo']

class ComercioViewSet(BaseModelViewSet):
    queryset = Comercio.objects.all()
    serializer_class = ComercioSerializer
    filterset_fields = ['produto', 'tipo']  # Campos válidos para Comercio
    search_fields = ['produto', 'tipo']
    ordering_fields = ['produto', 'tipo']

class ProcessamentoViewSet(BaseModelViewSet):
    queryset = Processamento.objects.all()
    serializer_class = ProcessamentoSerializer
    filterset_fields = ['produto', 'tipo']  # Campos válidos para Processamento
    search_fields = ['produto', 'tipo']
    ordering_fields = ['produto', 'tipo']

class ExportacaoViewSet(BaseModelViewSet):
    queryset = Exportacao.objects.all()
    serializer_class = ExportacaoSerializer
    filterset_fields = ['pais']  # Campos válidos para Exportacao
    search_fields = ['pais']
    ordering_fields = ['pais']

class ImportacaoViewSet(BaseModelViewSet):
    queryset = Importacao.objects.all()
    serializer_class = ImportacaoSerializer
    filterset_fields = ['pais']  # Campos válidos para Importacao
    search_fields = ['pais']
    ordering_fields = ['pais']

class AnoValorViewSet(viewsets.ModelViewSet):
    queryset = AnoValor.objects.all()
    serializer_class = AnoValorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['ano', 'valor', 'producao', 'comercio', 'processamento', 'exportacao', 'importacao']
    search_fields = ['ano', 'valor', 'producao', 'comercio', 'processamento', 'exportacao', 'importacao']
    ordering_fields = ['ano', 'valor', 'producao', 'comercio', 'processamento', 'exportacao', 'importacao']

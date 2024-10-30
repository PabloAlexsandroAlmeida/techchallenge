from rest_framework import viewsets, filters as drf_filters
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Producao, Comercializacao, Processamento, Exportacao, Importacao, Ano
from .serializers import (
    ProducaoSerializer,
    ComercializacaoSerializer,  # Corrigido de ComercioSerializer para ComercializacaoSerializer
    ProcessamentoSerializer,
    ExportacaoSerializer,
    ImportacaoSerializer,
    AnoSerializer,
)

class BaseModelViewSet(viewsets.ModelViewSet):
    """Base para ViewSets com permissões e filtros padrão."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]

# Filtro e ViewSet para Produção
class ProducaoFilter(filters.FilterSet):
    ano_min = filters.NumberFilter(field_name="ano__ano", lookup_expr='gte')
    ano_max = filters.NumberFilter(field_name="ano__ano", lookup_expr='lte')
    quantidade_min = filters.NumberFilter(field_name="quantidade", lookup_expr='gte')
    quantidade_max = filters.NumberFilter(field_name="quantidade", lookup_expr='lte')
    produto = filters.CharFilter(field_name="produto__nome", lookup_expr='icontains')

    class Meta:
        model = Producao
        fields = ['produto', 'ano_min', 'ano_max', 'quantidade_min', 'quantidade_max']

class ProducaoViewSet(BaseModelViewSet):
    queryset = Producao.objects.all()
    serializer_class = ProducaoSerializer
    filterset_class = ProducaoFilter

# Filtro e ViewSet para Comercialização (antigo Comercio)
class ComercializacaoFilter(filters.FilterSet):
    ano_min = filters.NumberFilter(field_name="ano__ano", lookup_expr='gte')
    ano_max = filters.NumberFilter(field_name="ano__ano", lookup_expr='lte')
    quantidade_min = filters.NumberFilter(field_name="quantidade", lookup_expr='gte')
    quantidade_max = filters.NumberFilter(field_name="quantidade", lookup_expr='lte')
    produto = filters.CharFilter(field_name="produto__nome", lookup_expr='icontains')

    class Meta:
        model = Comercializacao
        fields = ['produto', 'ano_min', 'ano_max', 'quantidade_min', 'quantidade_max']

class ComercializacaoViewSet(BaseModelViewSet):
    queryset = Comercializacao.objects.all()
    serializer_class = ComercializacaoSerializer
    filterset_class = ComercializacaoFilter

# Filtro e ViewSet para Processamento
class ProcessamentoFilter(filters.FilterSet):
    ano_min = filters.NumberFilter(field_name="ano__ano", lookup_expr='gte')
    ano_max = filters.NumberFilter(field_name="ano__ano", lookup_expr='lte')
    quantidade_min = filters.NumberFilter(field_name="quantidade", lookup_expr='gte')
    quantidade_max = filters.NumberFilter(field_name="quantidade", lookup_expr='lte')
    produto = filters.CharFilter(field_name="produto__nome", lookup_expr='icontains')

    class Meta:
        model = Processamento
        fields = ['produto', 'ano_min', 'ano_max', 'quantidade_min', 'quantidade_max']

class ProcessamentoViewSet(BaseModelViewSet):
    queryset = Processamento.objects.all()
    serializer_class = ProcessamentoSerializer
    filterset_class = ProcessamentoFilter

# Filtro e ViewSet para Exportação
class ExportacaoFilter(filters.FilterSet):
    ano_min = filters.NumberFilter(field_name="ano__ano", lookup_expr='gte')
    ano_max = filters.NumberFilter(field_name="ano__ano", lookup_expr='lte')
    quantidade_min = filters.NumberFilter(field_name="quantidade", lookup_expr='gte')
    quantidade_max = filters.NumberFilter(field_name="quantidade", lookup_expr='lte')
    produto = filters.CharFilter(field_name="produto__nome", lookup_expr='icontains')
    pais_nome = filters.CharFilter(field_name="pais__nome", lookup_expr='icontains')

    class Meta:
        model = Exportacao
        fields = ['produto', 'pais_nome', 'ano_min', 'ano_max', 'quantidade_min', 'quantidade_max']

class ExportacaoViewSet(BaseModelViewSet):
    queryset = Exportacao.objects.all()
    serializer_class = ExportacaoSerializer
    filterset_class = ExportacaoFilter

# Filtro e ViewSet para Importação
class ImportacaoFilter(filters.FilterSet):
    ano_min = filters.NumberFilter(field_name="ano__ano", lookup_expr='gte')
    ano_max = filters.NumberFilter(field_name="ano__ano", lookup_expr='lte')
    quantidade_min = filters.NumberFilter(field_name="quantidade", lookup_expr='gte')
    quantidade_max = filters.NumberFilter(field_name="quantidade", lookup_expr='lte')
    produto = filters.CharFilter(field_name="produto__nome", lookup_expr='icontains')
    pais_nome = filters.CharFilter(field_name="pais__nome", lookup_expr='icontains')

    class Meta:
        model = Importacao
        fields = ['produto', 'pais_nome', 'ano_min', 'ano_max', 'quantidade_min', 'quantidade_max']

class ImportacaoViewSet(BaseModelViewSet):
    queryset = Importacao.objects.all()
    serializer_class = ImportacaoSerializer
    filterset_class = ImportacaoFilter

# Filtro e ViewSet para Ano
class AnoViewSet(BaseModelViewSet):
    queryset = Ano.objects.all()
    serializer_class = AnoSerializer
    search_fields = ['ano']
    ordering_fields = ['ano']

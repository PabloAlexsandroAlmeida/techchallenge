from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import (
    Producao,
    Comercio,
    Processamento,
    Exportacao,
    Importacao,
    AnoValor,
)
from .serializers import (
    ProducaoSerializer,
    ComercioSerializer,
    ProcessamentoSerializer,
    ExportacaoSerializer,
    ImportacaoSerializer,
    AnoValorSerializer,
)

"""
Módulo de visualizações para a aplicação vitivinicultura.

Este módulo define os ViewSets para cada modelo, fornecendo endpoints
RESTful usando o Django REST Framework. Inclui capacidades de filtragem,
pesquisa e ordenação.
"""


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para modelos.

    Fornece permissões e backends de filtragem padrão.
    """

    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]


class ProdutoTipoViewSet(BaseModelViewSet):
    """
    ViewSet base para modelos com campos 'produto' e 'tipo'.

    Define campos padrão para filtragem, pesquisa e ordenação.
    """

    filterset_fields = ["produto", "tipo"]
    search_fields = ["produto", "tipo"]
    ordering_fields = ["produto", "tipo"]


class PaisViewSet(BaseModelViewSet):
    """
    ViewSet base para modelos com campo 'pais'.

    Define campos padrão para filtragem, pesquisa e ordenação.
    """

    filterset_fields = ["pais__nome"]
    search_fields = ["pais__nome"]
    ordering_fields = ["pais__nome"]


class ProducaoViewSet(ProdutoTipoViewSet):
    """
    ViewSet para o modelo Producao.

    Fornece ações padrão de listagem, criação, recuperação,
    atualização e exclusão.
    """

    queryset = Producao.objects.all()
    serializer_class = ProducaoSerializer


class ComercioViewSet(ProdutoTipoViewSet):
    """
    ViewSet para o modelo Comercio.

    Herda configurações padrão de ProdutoTipoViewSet.
    """

    queryset = Comercio.objects.all()
    serializer_class = ComercioSerializer


class ProcessamentoViewSet(ProdutoTipoViewSet):
    """
    ViewSet para o modelo Processamento.

    Herda configurações padrão de ProdutoTipoViewSet.
    """

    queryset = Processamento.objects.all()
    serializer_class = ProcessamentoSerializer


class ExportacaoViewSet(PaisViewSet):
    """
    ViewSet para o modelo Exportacao.

    Herda configurações padrão de PaisViewSet.
    """

    queryset = Exportacao.objects.all()
    serializer_class = ExportacaoSerializer


class ImportacaoViewSet(PaisViewSet):
    """
    ViewSet para o modelo Importacao.

    Herda configurações padrão de PaisViewSet.
    """

    queryset = Importacao.objects.all()
    serializer_class = ImportacaoSerializer


class AnoValorViewSet(BaseModelViewSet):
    """
    ViewSet para o modelo AnoValor.

    Fornece ações padrão e permite filtragem, pesquisa e ordenação
    por vários campos, incluindo campos relacionados.
    """

    queryset = AnoValor.objects.all()
    serializer_class = AnoValorSerializer

    # Campos disponíveis para filtragem, incluindo campos relacionados
    filterset_fields = [
        "ano",
        "valor",
        "tipo_valor",
        "producao__produto",
        "producao__tipo",
        "comercio__produto",
        "comercio__tipo",
        "processamento__produto",
        "processamento__tipo",
        "exportacao__pais__nome",
        "importacao__pais__nome",
    ]
    # Campos disponíveis para pesquisa
    search_fields = [
        "ano",
        "valor",
        "tipo_valor",
        "producao__produto",
        "producao__tipo",
        "comercio__produto",
        "comercio__tipo",
        "processamento__produto",
        "processamento__tipo",
        "exportacao__pais__nome",
        "importacao__pais__nome",
    ]
    # Campos disponíveis para ordenação
    ordering_fields = [
        "ano",
        "valor",
        "tipo_valor",
        "producao__produto",
        "producao__tipo",
        "comercio__produto",
        "comercio__tipo",
        "processamento__produto",
        "processamento__tipo",
        "exportacao__pais__nome",
        "importacao__pais__nome",
    ]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vitivinicultura.views import (
    ProducaoViewSet,
    ComercializacaoViewSet,  # Alterado de ComercioViewSet para ComercializacaoViewSet
    ProcessamentoViewSet,
    ExportacaoViewSet,
    ImportacaoViewSet,
    AnoViewSet,  # Alterado de AnoValorViewSet para AnoViewSet
)

"""
URL configuration for the vitivinicultura app.

Este arquivo define os padrões de URL para a API RESTful da aplicação,
utilizando o DefaultRouter do Django REST Framework para registrar os viewsets.
"""

# Criação do roteador padrão e registro dos viewsets
router = DefaultRouter()
router.register(r"producao", ProducaoViewSet, basename="producao")
router.register(r"comercializacao", ComercializacaoViewSet, basename="comercializacao")  # Alterado de comercio para comercializacao
router.register(r"processamento", ProcessamentoViewSet, basename="processamento")
router.register(r"exportacao", ExportacaoViewSet, basename="exportacao")
router.register(r"importacao", ImportacaoViewSet, basename="importacao")
router.register(r"ano", AnoViewSet, basename="ano")  # Alterado de anovalor para ano

# Definição dos padrões de URL
urlpatterns = [
    path("", include(router.urls)),
]

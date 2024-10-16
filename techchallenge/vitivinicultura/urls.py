from django.urls import path, include
from rest_framework.routers import DefaultRouter
from vitivinicultura.views import (
    ProducaoViewSet,
    ComercioViewSet,
    ProcessamentoViewSet,
    ExportacaoViewSet,
    ImportacaoViewSet,
    AnoValorViewSet,
)

"""
URL configuration for the vitivinicultura app.

Este arquivo define os padrões de URL para a API RESTful da aplicação,
utilizando o DefaultRouter do Django REST Framework para registrar os viewsets.
"""

# Criação do roteador padrão e registro dos viewsets
router = DefaultRouter()
router.register(r"producao", ProducaoViewSet, basename="producao")
router.register(r"comercio", ComercioViewSet, basename="comercio")
router.register(r"processamento", ProcessamentoViewSet, basename="processamento")
router.register(r"exportacao", ExportacaoViewSet, basename="exportacao")
router.register(r"importacao", ImportacaoViewSet, basename="importacao")
router.register(r"anovalor", AnoValorViewSet, basename="anovalor")

# Definição dos padrões de URL
urlpatterns = [
    path("", include(router.urls)),
]

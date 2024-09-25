from rest_framework.routers import DefaultRouter
from django.urls import path, include
from vitivinicultura.views import ProducaoViewSet, ComercioViewSet, ProcessamentoViewSet, ExportacaoViewSet, ImportacaoViewSet

router = DefaultRouter()
router.register(r'producao', ProducaoViewSet)
router.register(r'comercio', ComercioViewSet)
router.register(r'processamento', ProcessamentoViewSet)
router.register(r'exportacao', ExportacaoViewSet)
router.register(r'importacao', ImportacaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

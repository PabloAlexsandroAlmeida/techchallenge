from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProducaoViewSet, ComercioViewSet, ProcessamentoViewSet, ExportacaoViewSet, ImportacaoViewSet

router = DefaultRouter()
router.register(r'producao', ProducaoViewSet)
router.register(r'comercio', ComercioViewSet)
router.register(r'processamento', ProcessamentoViewSet)
router.register(r'exportacao', ExportacaoViewSet)
router.register(r'importacao', ImportacaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
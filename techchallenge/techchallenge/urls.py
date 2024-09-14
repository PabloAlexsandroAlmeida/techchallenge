from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from oauth2_provider.views import TokenView

schema_view = get_schema_view(
   openapi.Info(
      title="Vitivinicultura API",
      default_version='v1',
      description="Documentação da API de Vitivinicultura",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('vitivinicultura.urls')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   path('oauth/', include('oauth2_provider.urls', namespace='oauth2_provider')), 

]
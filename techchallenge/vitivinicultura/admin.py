from django.contrib import admin
from .models import Producao, Comercio, Processamento, Exportacao, Importacao, AnoValor

# Classe para exibir o modelo AnoValor no admin com mais detalhes
class AnoValorAdmin(admin.ModelAdmin):
    # Define quais campos serão exibidos na lista
    list_display = ('ano', 'valor', 'producao', 'comercio', 'processamento', 'exportacao', 'importacao')
    
    # Adiciona filtros laterais para facilitar a busca por ano ou valores específicos
    list_filter = ('ano', 'producao', 'comercio', 'processamento', 'exportacao', 'importacao')
    
    # Campos pelos quais será possível buscar na interface do admin
    search_fields = ('ano', 'valor', 'producao__produto', 'comercio__produto', 'processamento__produto', 'exportacao__produto', 'importacao__produto')

# Registra os modelos no admin
admin.site.register(Producao)
admin.site.register(Comercio)
admin.site.register(Processamento)
admin.site.register(Exportacao)
admin.site.register(Importacao)
admin.site.register(AnoValor, AnoValorAdmin)
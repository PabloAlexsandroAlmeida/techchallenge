from django.contrib import admin
from .models import Producao, Comercio, Processamento, Exportacao, Importacao, AnoValor

# Classe para exibir o modelo AnoValor no admin com mais detalhes
class AnoValorAdmin(admin.ModelAdmin):
    list_display = ('ano', 'valor', 'tipo_valor')
    list_filter = ('ano', 'tipo_valor')
    search_fields = ('ano', 'valor', 'tipo_valor')

# Registra os modelos no admin
admin.site.register(Producao)
admin.site.register(Comercio)
admin.site.register(Processamento)
admin.site.register(Exportacao)
admin.site.register(Importacao)
admin.site.register(AnoValor, AnoValorAdmin)

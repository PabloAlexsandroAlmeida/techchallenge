from django.contrib import admin
from .models import Producao, Comercializacao, Processamento, Exportacao, Importacao, Ano

# Classe para exibir o modelo Ano no admin com mais detalhes
class AnoAdmin(admin.ModelAdmin):
    list_display = ('ano',)
    list_filter = ('ano',)
    search_fields = ('ano',)

# Registra os modelos no admin
admin.site.register(Producao)
admin.site.register(Comercializacao)
admin.site.register(Processamento)
admin.site.register(Exportacao)
admin.site.register(Importacao)
admin.site.register(Ano, AnoAdmin)
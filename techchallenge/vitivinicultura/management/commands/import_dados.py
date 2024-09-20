import os
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from vitivinicultura.models import Producao, Comercio, Processamento, Exportacao, Importacao, AnoValor

# Função para carregar JSON do diretório data
def load_json(file_name):
    # Corrige o caminho para garantir que ele seja absoluto
    file_path = os.path.join(settings.BASE_DIR, 'vitivinicultura', 'data', file_name)
    with open(file_path, 'r') as f:
        return json.load(f)

# Função para verificar se um valor é numérico e não None
def is_valid_number(value):
    if value is None:
        return False
    try:
        float(value)  # Tenta converter para float
        return True
    except ValueError:
        return False

# Função para importar dados de produção
def import_producao(data):
    for item in data:
        producao_obj, created = Producao.objects.get_or_create(
            produto=item.get('produto', 'produto_desconhecido'),
            tipo=item.get('Tipo', 'tipo_desconhecido')
        )
        for ano, valor in item.items():
            if ano.isdigit():  # Verifica se é um ano
                if is_valid_number(valor):  # Apenas cria AnoValor se o valor for numérico
                    AnoValor.objects.create(
                        producao=producao_obj,
                        ano=int(ano),
                        valor=float(valor)
                    )

# Função para importar dados de comércio
def import_comercio(data):
    for item in data:
        comercio_obj, created = Comercio.objects.get_or_create(
            produto=item.get('Produto', 'produto_desconhecido'),
            tipo=item.get('Tipo', 'tipo_desconhecido')
        )
        for ano, valor in item.items():
            if ano.isdigit():
                if is_valid_number(valor):  # Verifica se é um número
                    AnoValor.objects.create(
                        comercio=comercio_obj,
                        ano=int(ano),
                        valor=float(valor)
                    )

# Função para importar dados de processamento
def import_processamento(data):
    for item in data:
        processamento_obj, created = Processamento.objects.get_or_create(
            produto=item.get('Produto', 'produto_desconhecido'),
            tipo=item.get('Tipo', 'tipo_desconhecido')
        )
        for ano, valor in item.items():
            if ano.isdigit():
                if is_valid_number(valor):  # Verifica se é um número
                    AnoValor.objects.create(
                        processamento=processamento_obj,
                        ano=int(ano),
                        valor=float(valor)
                    )

# Função para importar dados de exportação
def import_exportacao(data):
    for item in data:
        exportacao_obj, created = Exportacao.objects.get_or_create(
            produto=item.get('Produto', 'produto_desconhecido'),
            tipo=item.get('Tipo', 'tipo_desconhecido')
        )
        for ano, valor in item.items():
            if ano.isdigit():
                if is_valid_number(valor):  # Verifica se é um número
                    AnoValor.objects.create(
                        exportacao=exportacao_obj,
                        ano=int(ano),
                        valor=float(valor)
                    )

# Função para importar dados de importação
def import_importacao(data):
    for item in data:
        importacao_obj, created = Importacao.objects.get_or_create(
            produto=item.get('Produto', 'produto_desconhecido'),
            tipo=item.get('Tipo', 'tipo_desconhecido')
        )
        for ano, valor in item.items():
            if ano.isdigit():
                if is_valid_number(valor):  # Verifica se é um número
                    AnoValor.objects.create(
                        importacao=importacao_obj,
                        ano=int(ano),
                        valor=float(valor)
                    )

class Command(BaseCommand):
    help = 'Importa dados dos arquivos JSON para o banco de dados'

    def handle(self, *args, **kwargs):
        producao_data = load_json('producao_sanitizado.json')
        comercio_data = load_json('comercio_sanitizado.json')
        processamento_data = load_json('processamento_sanitizado.json')
        exportacao_data = load_json('exportacao_sanitizado.json')
        importacao_data = load_json('importacao_sanitizado.json')

        import_producao(producao_data)
        import_comercio(comercio_data)
        import_processamento(processamento_data)
        import_exportacao(exportacao_data)
        import_importacao(importacao_data)

        self.stdout.write(self.style.SUCCESS('Importação de dados concluída com sucesso!'))

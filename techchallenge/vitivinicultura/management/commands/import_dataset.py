import os
import json
import unicodedata
from typing import Any, Dict, List, Type
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from vitivinicultura.models import (
    Producao, Comercio, Processamento, Exportacao, Importacao, AnoValor, Pais
)

def normalize_key(key: str) -> str:
    key = key.lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', key)
        if unicodedata.category(c) != 'Mn'
    )

def load_json(file_name: str) -> List[Dict[str, Any]]:
    """
    Carrega um arquivo JSON localizado no diretório 'data' da aplicação.
    """
    file_path = os.path.join(settings.BASE_DIR, 'vitivinicultura', 'data', file_name)
    with open(file_path, 'r') as f:
        return json.load(f)

def is_valid_number(value: Any) -> bool:
    """
    Verifica se o valor fornecido pode ser convertido em um número float.
    """
    try:
        return float(value) is not None
    except (TypeError, ValueError):
        return False

def import_data(
    data: List[Dict[str, Any]],
    model: Type[Any],
    model_fields: List[str],
    ano_valor_field_name: str,
    field_mappings: Dict[str, str] = None  # Novo parâmetro para mapeamento de campos
) -> None:
    with transaction.atomic():
        try:
            # Limpa todos os registros existentes no modelo e em AnoValor relacionado
            AnoValor.objects.filter(**{ano_valor_field_name + '__isnull': False}).delete()
            model.objects.all().delete()

            for item in data:
                # Normaliza as chaves para minúsculas e remove acentos
                item_normalized = {normalize_key(k): v for k, v in item.items()}

                # Aplica mapeamentos de campos, se fornecidos
                if field_mappings:
                    for original_field, mapped_field in field_mappings.items():
                        if original_field in item_normalized:
                            item_normalized[mapped_field] = item_normalized.pop(original_field)

                # Tratamento especial para o campo 'pais'
                if 'pais' in item_normalized:
                    pais_nome = item_normalized['pais']
                    pais_obj, _ = Pais.objects.get_or_create(nome=pais_nome)
                    item_normalized['pais'] = pais_obj  # Substitui pelo objeto Pais

                # Prepara os argumentos para get_or_create
                get_or_create_kwargs = {
                    field: item_normalized[field]
                    for field in model_fields
                    if field in item_normalized
                }

                # Verifica se todos os campos necessários estão presentes
                for field in model_fields:
                    if field not in get_or_create_kwargs:
                        raise ValueError(f"O campo obrigatório '{field}' está ausente nos dados.")

                obj, created = model.objects.get_or_create(**get_or_create_kwargs)

                # Verifica se o dado possui o campo 'ano'
                if 'ano' in item_normalized:
                    ano = item_normalized['ano']
                    if is_valid_number(ano):
                        valor_fields = ['valor_usd', 'quantidade']
                        for valor_field in valor_fields:
                            if valor_field in item_normalized and is_valid_number(item_normalized[valor_field]):
                                valor = float(item_normalized[valor_field])
                                tipo_valor = valor_field  # 'valor_usd' ou 'quantidade'
                                ano_valor = AnoValor.objects.create(
                                    **{ano_valor_field_name: obj},
                                    ano=int(ano),
                                    valor=valor,
                                    tipo_valor=tipo_valor
                                )
                else:
                    # Processa o formato original onde os anos são chaves
                    for ano, valor in item_normalized.items():
                        if ano.isdigit() and is_valid_number(valor):
                            ano_valor = AnoValor.objects.create(
                                **{ano_valor_field_name: obj},
                                ano=int(ano),
                                valor=float(valor),
                                tipo_valor='valor'
                            )
        except Exception as e:
            print(f"Ocorreu um erro durante a importação: {e}")
            raise


class Command(BaseCommand):
    """
    Comando customizado do Django para importar dados de arquivos JSON para o banco de dados.
    """
    help = 'Importa dados dos arquivos JSON para o banco de dados'

    def handle(self, *args, **kwargs) -> None:
        """
        Método principal que executa a importação dos dados.
        """
        # Lista de fontes de dados com suas configurações
        data_sources = [
            {
                'file_name': 'producao_sanitizado.json',
                'model': Producao,
                'model_fields': ['produto', 'tipo'],
                'ano_valor_field_name': 'producao',
            },
            {
                'file_name': 'comercio_sanitizado.json',
                'model': Comercio,
                'model_fields': ['produto', 'tipo'],
                'ano_valor_field_name': 'comercio',
            },
            {
                'file_name': 'processamento_sanitizado.json',
                'model': Processamento,
                'model_fields': ['produto', 'tipo'],
                'ano_valor_field_name': 'processamento',
                'field_mappings': {'cultivar': 'produto'}  # Mapeia 'cultivar' para 'produto'
            },
            {
                'file_name': 'exportacao_sanitizado.json',
                'model': Exportacao,
                'model_fields': ['pais'],
                'ano_valor_field_name': 'exportacao',
            },
            {
                'file_name': 'importacao_sanitizado.json',
                'model': Importacao,
                'model_fields': ['pais'],
                'ano_valor_field_name': 'importacao',
            },
        ]


        # Itera sobre cada fonte de dados e realiza a importação
        for source in data_sources:
            data = load_json(source['file_name'])
            import_data(
                data=data,
                model=source['model'],
                model_fields=source['model_fields'],
                ano_valor_field_name=source['ano_valor_field_name'],
                field_mappings=source.get('field_mappings')  # Passa o mapeamento de campos, se existir
            )

        self.stdout.write(self.style.SUCCESS('Importação de dados concluída com sucesso!'))

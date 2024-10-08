import os
import json
from typing import Any, Dict, List, Type
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from vitivinicultura.models import (
    Producao, Comercio, Processamento, Exportacao, Importacao, AnoValor
)


def load_json(file_name: str) -> List[Dict[str, Any]]:
    """
    Carrega um arquivo JSON localizado no diretório 'data' da aplicação.

    Args:
        file_name (str): Nome do arquivo JSON a ser carregado.

    Returns:
        List[Dict[str, Any]]: Dados carregados do arquivo JSON.
    """
    file_path = os.path.join(settings.BASE_DIR, 'vitivinicultura', 'data', file_name)
    with open(file_path, 'r') as f:
        return json.load(f)


def is_valid_number(value: Any) -> bool:
    """
    Verifica se o valor fornecido pode ser convertido em um número float.

    Args:
        value (Any): O valor a ser verificado.

    Returns:
        bool: True se o valor for um número válido, False caso contrário.
    """
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def get_field_value(item: Dict[str, Any], field_name: str, default: Any = None) -> Any:
    """
    Obtém o valor de um campo do dicionário, lidando com diferentes capitalizações.

    Args:
        item (Dict[str, Any]): Dicionário contendo os dados.
        field_name (str): Nome do campo a ser extraído.
        default (Any, opcional): Valor padrão caso o campo não exista.

    Returns:
        Any: Valor do campo ou valor padrão.
    """
    return item.get(field_name.lower(), item.get(field_name.capitalize(), default))


def import_data(
    data: List[Dict[str, Any]],
    model: Type[Any],
    model_fields: List[str],
    ano_valor_field_name: str
) -> None:
    """
    Importa dados para o modelo especificado e cria instâncias relacionadas de AnoValor.

    Args:
        data (List[Dict[str, Any]]): Dados a serem importados.
        model (Type[Any]): Modelo Django onde os dados serão inseridos.
        model_fields (List[str]): Campos do modelo a serem considerados.
        ano_valor_field_name (str): Nome do campo relacionado em AnoValor.
    """
    with transaction.atomic():
        # Limpa todos os registros existentes no modelo e em AnoValor relacionado
        AnoValor.objects.filter(**{ano_valor_field_name + '__isnull': False}).delete()
        model.objects.all().delete()

        for item in data:
            # Normaliza as chaves para minúsculas
            item_normalized = {k.lower(): v for k, v in item.items()}

            # Prepara os argumentos para get_or_create
            get_or_create_kwargs = {
                field: get_field_value(item_normalized, field, f'{field}_desconhecido')
                for field in model_fields
            }
            obj, _ = model.objects.get_or_create(**get_or_create_kwargs)

            # Prepara a lista de objetos AnoValor a serem criados
            ano_valor_objects = []
            for ano, valor in item.items():
                if ano.isdigit() and is_valid_number(valor):
                    ano_valor_objects.append(
                        AnoValor(
                            **{ano_valor_field_name: obj},
                            ano=int(ano),
                            valor=float(valor)
                        )
                    )

            # Cria os objetos AnoValor em massa
            AnoValor.objects.bulk_create(ano_valor_objects)


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
            },
            {
                'file_name': 'exportacao_sanitizado.json',
                'model': Exportacao,
                'model_fields': ['produto', 'tipo'],
                'ano_valor_field_name': 'exportacao',
            },
            {
                'file_name': 'importacao_sanitizado.json',
                'model': Importacao,
                'model_fields': ['produto', 'tipo'],
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
                ano_valor_field_name=source['ano_valor_field_name']
            )

        self.stdout.write(self.style.SUCCESS('Importação de dados concluída com sucesso!'))
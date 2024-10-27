import os
import json
import unicodedata
import logging
from typing import Any, Dict, List, Type, Optional
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from vitivinicultura.models import (
    Producao,
    Comercio,
    Processamento,
    Exportacao,
    Importacao,
    AnoValor,
    Pais,
)

# Configuração do logger
logger = logging.getLogger(__name__)


def normalize_key(key: str) -> str:
    """
    Normaliza uma chave de dicionário, convertendo-a para minúsculas e removendo acentuação.

    Args:
        key (str): A chave a ser normalizada.

    Returns:
        str: A chave normalizada.
    """
    normalized_key = key.lower()
    return "".join(
        c
        for c in unicodedata.normalize("NFD", normalized_key)
        if unicodedata.category(c) != "Mn"
    )


def load_json(file_name: str) -> List[Dict[str, Any]]:
    """
    Carrega um arquivo JSON localizado no diretório 'data' da aplicação.

    Args:
        file_name (str): Nome do arquivo JSON a ser carregado.

    Returns:
        List[Dict[str, Any]]: Lista de dicionários contendo os dados do JSON.

    Raises:
        FileNotFoundError: Se o arquivo não for encontrado.
        json.JSONDecodeError: Se ocorrer um erro ao decodificar o JSON.
    """
    file_path = os.path.join(settings.BASE_DIR, "vitivinicultura", "data", file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.info(f"Arquivo '{file_name}' carregado com sucesso.")
            return data
    except FileNotFoundError as e:
        logger.error(f"Arquivo '{file_name}' não encontrado: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Erro ao decodificar o arquivo '{file_name}': {e}")
        raise


def is_valid_number(value: Any) -> bool:
    """
    Verifica se o valor fornecido pode ser convertido em um número float.

    Args:
        value (Any): O valor a ser verificado.

    Returns:
        bool: True se o valor pode ser convertido em float, False caso contrário.
    """
    try:
        float(value)
        return True
    except (TypeError, ValueError):
        return False


def import_data(
    data: List[Dict[str, Any]],
    model: Type[Any],
    model_fields: List[str],
    ano_valor_field_name: str,
    field_mappings: Optional[Dict[str, str]] = None,
) -> None:
    """
    Importa dados para o banco de dados, criando instâncias dos modelos especificados.

    Args:
        data (List[Dict[str, Any]]): Dados a serem importados.
        model (Type[Any]): Modelo Django onde os dados serão inseridos.
        model_fields (List[str]): Campos obrigatórios do modelo.
        ano_valor_field_name (str): Nome do campo relacionado ao modelo AnoValor.
        field_mappings (Optional[Dict[str, str]], optional): Mapeamento de campos, se necessário.

    Raises:
        ValueError: Se campos obrigatórios estiverem ausentes nos dados.
        Exception: Para outros erros não previstos.
    """
    with transaction.atomic():
        try:
            # Limpa todos os registros existentes no modelo e em AnoValor relacionado
            AnoValor.objects.filter(
                **{f"{ano_valor_field_name}__isnull": False}
            ).delete()
            model.objects.all().delete()
            logger.info(f"Registros antigos removidos para o modelo {model.__name__}.")

            for item in data:
                # Normaliza as chaves para minúsculas e remove acentos
                item_normalized = {normalize_key(k): v for k, v in item.items()}

                # Aplica mapeamentos de campos, se fornecidos
                if field_mappings:
                    for original_field, mapped_field in field_mappings.items():
                        if original_field in item_normalized:
                            item_normalized[mapped_field] = item_normalized.pop(
                                original_field
                            )
                            logger.debug(
                                f"Campo '{original_field}' mapeado para '{mapped_field}'."
                            )

                # Tratamento especial para o campo 'pais'
                if "pais" in item_normalized:
                    pais_nome = item_normalized["pais"]
                    pais_obj, _ = Pais.objects.get_or_create(nome=pais_nome)
                    item_normalized["pais"] = pais_obj  # Substitui pelo objeto Pais
                    logger.debug(f"Objeto Pais criado ou recuperado: {pais_nome}")

                # Prepara os argumentos para get_or_create
                get_or_create_kwargs = {
                    field: item_normalized[field]
                    for field in model_fields
                    if field in item_normalized
                }

                # Verifica se todos os campos necessários estão presentes
                missing_fields = [
                    field for field in model_fields if field not in get_or_create_kwargs
                ]
                if missing_fields:
                    error_msg = f"Campos obrigatórios ausentes: {missing_fields}"
                    logger.error(error_msg)
                    raise ValueError(error_msg)

                obj, created = model.objects.get_or_create(**get_or_create_kwargs)
                action = "Criado" if created else "Atualizado"
                logger.debug(f"{action} objeto {model.__name__}: {obj}")

                # Processa os campos de ano e valor
                if "ano" in item_normalized:
                    ano = item_normalized["ano"]
                    if is_valid_number(ano):
                        valor_fields = ["valor_usd", "quantidade"]
                        for valor_field in valor_fields:
                            if valor_field in item_normalized and is_valid_number(
                                item_normalized[valor_field]
                            ):
                                valor = float(item_normalized[valor_field])
                                tipo_valor = valor_field  # 'valor_usd' ou 'quantidade'
                                AnoValor.objects.create(
                                    **{ano_valor_field_name: obj},
                                    ano=int(float(ano)),
                                    valor=valor,
                                    tipo_valor=tipo_valor,
                                )
                                logger.debug(
                                    f"AnoValor criado: {ano}, valor: {valor}, tipo: {tipo_valor}"
                                )
                else:
                    # Processa o formato onde os anos são chaves
                    for ano, valor in item_normalized.items():
                        if ano.isdigit() and is_valid_number(valor):
                            AnoValor.objects.create(
                                **{ano_valor_field_name: obj},
                                ano=int(ano),
                                valor=float(valor),
                                tipo_valor="valor",
                            )
                            logger.debug(
                                f"AnoValor criado: {ano}, valor: {valor}, tipo: 'valor'"
                            )
        except Exception as e:
            logger.error(f"Ocorreu um erro durante a importação: {e}")
            raise


class Command(BaseCommand):
    """
    Comando customizado do Django para importar dados de arquivos JSON para o banco de dados.

    Este comando realiza as tratativas finais nos dados e importa os dados sanitizados para o banco de dados,
    criando as instâncias dos modelos correspondentes.
    """

    help = "Dataset Stage 2: Importa dados de arquivos JSON para o banco de dados."

    def handle(self, *args, **kwargs) -> None:
        """
        Método principal que executa a importação dos dados.

        Itera sobre uma lista de fontes de dados, carregando cada arquivo JSON e importando os dados
        para o banco de dados usando a função 'import_data'.
        """
        # Configuração do logger dentro do comando
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)

        # Lista de fontes de dados com suas configurações
        data_sources = [
            {
                "file_name": "producao_sanitizado.json",
                "model": Producao,
                "model_fields": ["produto", "tipo"],
                "ano_valor_field_name": "producao",
            },
            {
                "file_name": "comercio_sanitizado.json",
                "model": Comercio,
                "model_fields": ["produto", "tipo"],
                "ano_valor_field_name": "comercio",
            },
            {
                "file_name": "processamento_sanitizado.json",
                "model": Processamento,
                "model_fields": ["produto", "tipo"],
                "ano_valor_field_name": "processamento",
                "field_mappings": {
                    "cultivar": "produto"
                },  # Mapeia 'cultivar' para 'produto'
            },
            {
                "file_name": "exportacao_sanitizado.json",
                "model": Exportacao,
                "model_fields": ["pais"],
                "ano_valor_field_name": "exportacao",
            },
            {
                "file_name": "importacao_sanitizado.json",
                "model": Importacao,
                "model_fields": ["pais"],
                "ano_valor_field_name": "importacao",
            },
        ]

        # Itera sobre cada fonte de dados e realiza a importação
        for source in data_sources:
            try:
                logger.info(
                    f"Iniciando importação para o arquivo '{source['file_name']}'..."
                )
                data = load_json(source["file_name"])
                import_data(
                    data=data,
                    model=source["model"],
                    model_fields=source["model_fields"],
                    ano_valor_field_name=source["ano_valor_field_name"],
                    field_mappings=source.get("field_mappings"),
                )
                logger.info(f"Importação concluída para '{source['file_name']}'.")
            except Exception as e:
                logger.error(f"Erro ao importar '{source['file_name']}': {e}")
                continue  # Prossegue para o próximo arquivo

        self.stdout.write(
            self.style.SUCCESS("Importação de dados concluída com sucesso!")
        )

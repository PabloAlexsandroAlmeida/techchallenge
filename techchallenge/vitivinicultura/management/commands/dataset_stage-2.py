import os
import json
import unicodedata
import logging
from typing import Any, Dict, List, Type, Optional
from django.core.management.base import BaseCommand
from django.db import transaction
from vitivinicultura.models import (
    Producao,
    Comercializacao,
    Processamento,
    Exportacao,
    Importacao,
    Ano,
    Pais,
    Produto,
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
    file_path = os.path.join("./techchallenge/vitivinicultura/data/", file_name)
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
    field_mappings: Optional[Dict[str, str]] = None,
    default_values: Optional[Dict[str, Any]] = None,
) -> None:
    """
    Importa dados para o banco de dados, criando instâncias dos modelos especificados.

    Args:
        data (List[Dict[str, Any]]): Dados a serem importados.
        model (Type[Any]): Modelo Django onde os dados serão inseridos.
        model_fields (List[str]): Campos obrigatórios do modelo.
        field_mappings (Optional[Dict[str, str]], optional): Mapeamento de campos, se necessário.
        default_values (Optional[Dict[str, Any]], optional): Valores padrão para campos ausentes.

    Raises:
        ValueError: Se campos obrigatórios estiverem ausentes nos dados.
        Exception: Para outros erros não previstos.
    """
    with transaction.atomic():
        try:
            # Limpa todos os registros existentes no modelo
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
                    item_normalized["pais"] = pais_obj
                    logger.debug(f"Objeto Pais criado ou recuperado: {pais_nome}")

                # Tratamento para 'produto' e 'tipo'
                default_values = default_values or {}
                produto_nome = item_normalized.get("produto") or default_values.get(
                    "produto_nome"
                )
                produto_tipo = item_normalized.get("tipo") or default_values.get(
                    "produto_tipo"
                )

                if produto_nome and produto_tipo:
                    produto_obj, created = Produto.objects.get_or_create(
                        nome=produto_nome, tipo=produto_tipo
                    )
                    item_normalized["produto"] = produto_obj
                    logger.debug(
                        f"Objeto Produto {'criado' if created else 'recuperado'}: {produto_obj} (ID: {produto_obj.id})"
                    )
                else:
                    error_msg = (
                        "Informações do produto ausentes nos dados e em default_values."
                    )
                    logger.error(error_msg)
                    raise ValueError(error_msg)

                # Verifica se 'ano' está nos dados
                if "ano" in item_normalized:
                    # Tratamento quando 'ano' está nos dados
                    ano_value = int(float(item_normalized["ano"]))
                    ano_obj, _ = Ano.objects.get_or_create(ano=ano_value)
                    item_normalized["ano"] = ano_obj
                    logger.debug(f"Objeto Ano criado ou recuperado: {ano_value}")

                    # Prepara os argumentos para update_or_create
                    get_or_create_kwargs = {
                        field: item_normalized[field]
                        for field in model_fields
                        if field in item_normalized
                    }

                    # Processa os campos de quantidade e valor
                    extra_fields = {}
                    if "quantidade" in item_normalized:
                        if is_valid_number(item_normalized["quantidade"]):
                            extra_fields["quantidade"] = float(
                                item_normalized["quantidade"]
                            )
                        else:
                            extra_fields["quantidade"] = None  # Ou 0.0
                            logger.warning(
                                f"Valor inválido para 'quantidade'; definindo como None."
                            )
                    if "valor" in item_normalized:
                        if is_valid_number(item_normalized["valor"]):
                            extra_fields["valor"] = float(item_normalized["valor"])
                        else:
                            extra_fields["valor"] = None  # Ou 0.0
                            logger.warning(
                                f"Valor inválido para 'valor'; definindo como None."
                            )
                    if "valor_usd" in item_normalized:
                        if is_valid_number(item_normalized["valor_usd"]):
                            extra_fields["valor"] = float(item_normalized["valor_usd"])
                        else:
                            extra_fields["valor"] = None  # Ou 0.0
                            logger.warning(
                                f"Valor inválido para 'valor_usd'; definindo como None."
                            )

                    # Cria ou atualiza a instância do modelo
                    obj, created = model.objects.update_or_create(
                        **get_or_create_kwargs, defaults=extra_fields
                    )
                    action = "Criado" if created else "Atualizado"
                    logger.debug(f"{action} objeto {model.__name__}: {obj}")

                else:
                    # Caso os anos sejam chaves nos dados
                    # Lista de campos que não são anos
                    non_year_fields = set(
                        model_fields
                        + [
                            "quantidade",
                            "valor",
                            "valor_usd",
                            "produto",
                            "pais",
                            "id",
                            "tipo",
                        ]
                    )

                    # Filtra apenas as chaves que representam anos
                    year_data = {
                        k: v
                        for k, v in item_normalized.items()
                        if k not in non_year_fields and k.isdigit()
                    }

                    if not year_data:
                        error_msg = "Anos ausentes nos dados e nenhum ano encontrado como chave."
                        logger.error(error_msg)
                        raise ValueError(error_msg)

                    for ano_str, valor in year_data.items():
                        ano_value = int(ano_str)
                        ano_obj, _ = Ano.objects.get_or_create(ano=ano_value)
                        logger.debug(f"Objeto Ano criado ou recuperado: {ano_value}")

                        # Prepara os argumentos para update_or_create
                        get_or_create_kwargs = {
                            field: item_normalized[field]
                            for field in model_fields
                            if field in item_normalized and field != "ano"
                        }
                        get_or_create_kwargs["ano"] = ano_obj

                        # Processa os campos de quantidade e valor
                        extra_fields = {}
                        if is_valid_number(valor):
                            extra_fields["quantidade"] = float(valor)
                        else:
                            extra_fields["quantidade"] = None  # Ou 0.0
                            logger.warning(
                                f"Valor '{valor}' para o ano '{ano_str}' não é um número válido."
                            )

                        # Cria ou atualiza a instância do modelo
                        obj, created = model.objects.update_or_create(
                            **get_or_create_kwargs, defaults=extra_fields
                        )
                        action = "Criado" if created else "Atualizado"
                        logger.debug(f"{action} objeto {model.__name__}: {obj}")

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
                "model_fields": ["produto", "ano"],
                "field_mappings": {},
                "default_values": {"produto_tipo": "Produção"},
            },
            {
                "file_name": "comercio_sanitizado.json",
                "model": Comercializacao,
                "model_fields": ["produto", "ano"],
                "field_mappings": {},
                "default_values": {"produto_tipo": "Comercialização"},
            },
            {
                "file_name": "processamento_sanitizado.json",
                "model": Processamento,
                "model_fields": ["produto", "ano"],
                "field_mappings": {"cultivar": "produto"},
                "default_values": {"produto_tipo": "Processamento"},
            },
            {
                "file_name": "processamento_americanas_sanitizado.json",
                "model": Processamento,
                "model_fields": ["produto", "ano"],
                "field_mappings": {"cultivar": "produto"},
                "default_values": {"produto_tipo": "Processamento Americanas"},
            },
            {
                "file_name": "processamento_mesa_sanitizado.json",
                "model": Processamento,
                "model_fields": ["produto", "ano"],
                "field_mappings": {"cultivar": "produto"},
                "default_values": {"produto_tipo": "Processamento Mesa"},
            },
            {
                "file_name": "processamento_semclass_sanitizado.json",
                "model": Processamento,
                "model_fields": ["produto", "ano"],
                "field_mappings": {"cultivar": "produto"},
                "default_values": {
                    "produto_tipo": "Processamento Sem Classificação"
                },
            },
            {
                "file_name": "exportacao_sanitizado.json",
                "model": Exportacao,
                "model_fields": ["pais", "produto", "ano"],
                "field_mappings": {},
                "default_values": {"produto_nome": "Vinho", "produto_tipo": "Bebida"},
            },
            {
                "file_name": "exportacao_espumantes_sanitizado.json",
                "model": Exportacao,
                "model_fields": ["pais", "produto", "ano"],
                "field_mappings": {},
                "default_values": {
                    "produto_nome": "Espumante",
                    "produto_tipo": "Bebida",
                },
            },
            {
                "file_name": "exportacao_uva_sanitizado.json",
                "model": Exportacao,
                "model_fields": ["pais", "produto", "ano"],
                "field_mappings": {},
                "default_values": {"produto_nome": "Uva", "produto_tipo": "Fruta"},
            },
            {
                "file_name": "exportacao_suco_sanitizado.json",
                "model": Exportacao,
                "model_fields": ["pais", "produto", "ano"],
                "field_mappings": {},
                "default_values": {"produto_nome": "Suco", "produto_tipo": "Bebida"},
            },
            {
                "file_name": "importacao_sanitizado.json",
                "model": Importacao,
                "model_fields": ["pais", "produto", "ano"],
                "field_mappings": {},
                "default_values": {"produto_nome": "Vinho", "produto_tipo": "Bebida"},
            },
            {
                "file_name": "importacao_espumantes_sanitizado.json",
                "model": Importacao,
                "model_fields": ["pais", "produto", "ano"],
                "field_mappings": {},
                "default_values": {
                    "produto_nome": "Espumante",
                    "produto_tipo": "Bebida",
                },
            },
            {
                "file_name": "importacao_frescas_sanitizado.json",
                "model": Importacao,
                "model_fields": ["pais", "produto", "ano"],
                "field_mappings": {},
                "default_values": {
                    "produto_nome": "Uva Fresca",
                    "produto_tipo": "Fruta",
                },
            },
            {
                "file_name": "importacao_passas_sanitizado.json",
                "model": Importacao,
                "model_fields": ["pais", "produto", "ano"],
                "field_mappings": {},
                "default_values": {
                    "produto_nome": "Uva Passa",
                    "produto_tipo": "Fruta",
                },
            },
            {
                "file_name": "importacao_suco_sanitizado.json",
                "model": Importacao,
                "model_fields": ["pais", "produto", "ano"],
                "field_mappings": {},
                "default_values": {"produto_nome": "Suco", "produto_tipo": "Bebida"},
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
                    field_mappings=source.get("field_mappings"),
                    default_values=source.get("default_values", {}),
                )
                logger.info(f"Importação concluída para '{source['file_name']}'.")
            except Exception as e:
                logger.error(f"Erro ao importar '{source['file_name']}': {e}")
                continue  # Prossegue para o próximo arquivo

        self.stdout.write(
            self.style.SUCCESS("Importação de dados concluída com sucesso!")
        )

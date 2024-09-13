import os
import json
import requests
import pandas as pd
from io import StringIO
import logging
from typing import Dict, Any, Union

# Configurar o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SanitizadorDataset:
    def __init__(self, config):
        """
        Classe base para sanitização de datasets.

        :param config: Dicionário com a configuração do dataset.
        """
        self.url = config.get('url')
        self.caminho_saida = config.get('caminho_saida', '.')
        self.delimitador = config.get('delimitador', ';')
        self.codificacao = config.get('codificacao', 'utf-8')
        self.columns_to_drop = config.get('columns_to_drop', [])
        self.nome_coluna = config.get('nome_coluna')
        self.coluna_grupo = config.get('coluna_grupo', 'Tipo')
        self.special_processing = config.get('special_processing')
        self.df = None

    def baixar_e_carregar_csv(self):
        """
        Baixa um arquivo CSV da URL fornecida e carrega em um DataFrame pandas.
        """
        try:
            logger.info(f"Baixando arquivo de: {self.url}")
            resposta = requests.get(self.url)
            resposta.raise_for_status()

            # Garantir que o diretório de saída existe
            os.makedirs(self.caminho_saida, exist_ok=True)

            # Salvar o arquivo original diretamente no disco
            nome_arquivo_original = os.path.basename(self.url)
            caminho_arquivo_original = os.path.join(self.caminho_saida, nome_arquivo_original)

            with open(caminho_arquivo_original, 'wb') as f:
                f.write(resposta.content)
            logger.info(f"Arquivo original salvo com sucesso em: {caminho_arquivo_original}")

            # Decodificar o conteúdo baixado
            dados_csv = resposta.content.decode(self.codificacao)

            # Carregar o CSV usando a string decodificada
            self.df = pd.read_csv(StringIO(dados_csv), delimiter=self.delimitador)
            logger.info(f"Arquivo baixado e carregado com sucesso: {self.url}")
        except Exception as e:
            logger.error(f"Erro ao baixar ou carregar o arquivo de {self.url}: {e}")
            raise

    def salvar_csv(self, df_sanitizado: pd.DataFrame, nome_arquivo: str) -> None:
        """
        Salva o DataFrame sanitizado em um arquivo CSV.

        :param df_sanitizado: O DataFrame pandas sanitizado.
        :param nome_arquivo: O nome do arquivo para salvar o CSV.
        """
        try:
            caminho_saida = os.path.join(self.caminho_saida, nome_arquivo)
            df_sanitizado.to_csv(caminho_saida, index=False)
            logger.info(f"CSV sanitizado salvo com sucesso em: {caminho_saida}")
        except Exception as e:
            logger.error(f"Erro ao salvar o arquivo CSV sanitizado: {e}")
            raise

    def salvar_json(self, dados: Union[pd.DataFrame, Dict[Any, Any]], nome_arquivo: str) -> None:
        """
        Salva os dados sanitizados em um arquivo JSON.

        :param dados: Os dados sanitizados como um DataFrame pandas ou um dicionário.
        :param nome_arquivo: O nome do arquivo para salvar o JSON.
        """
        try:
            caminho_saida = os.path.join(self.caminho_saida, nome_arquivo)
            with open(caminho_saida, 'w', encoding='utf-8') as f:
                if isinstance(dados, pd.DataFrame):
                    dados.to_json(f, orient='records', force_ascii=False)
                else:
                    json.dump(dados, f, indent=4, ensure_ascii=False)
            logger.info(f"JSON sanitizado salvo com sucesso em: {caminho_saida}")
        except Exception as e:
            logger.error(f"Erro ao salvar o arquivo JSON sanitizado: {e}")
            raise

    def sanitizar(self):
        """
        Sanitiza o dataset com base nas configurações fornecidas.
        """
        try:
            logger.info("Iniciando sanitização do arquivo")
            if self.columns_to_drop:
                self.df = self.df.drop(columns=self.columns_to_drop)
            if self.special_processing == 'importacao_exportacao':
                self._sanitizar_importacao_exportacao()
            else:
                df_sanitizado = self._sanitizar_grupos_maiusculos(
                    nome_coluna=self.nome_coluna,
                    coluna_grupo=self.coluna_grupo
                )
                if self.special_processing == 'comercio_outros_vinhos':
                    # Processamento especial para 'Comercio'
                    df_sanitizado['Produto'] = df_sanitizado['Produto'].str.strip()
                    indices_outros = df_sanitizado[
                        df_sanitizado['Produto'].str.contains("Outros vinhos", case=False, na=False)
                    ].index
                    if not indices_outros.empty:
                        indice_inicio = indices_outros[0]
                        df_sanitizado.loc[indice_inicio:, 'Tipo'] = "OUTROS"
                self.df = df_sanitizado
            logger.info("Sanitização concluída")
            return self.df
        except Exception as e:
            logger.error(f"Erro durante a sanitização: {e}")
            raise

    def _sanitizar_grupos_maiusculos(self, nome_coluna: str, coluna_grupo: str = 'Tipo') -> pd.DataFrame:
        """
        Sanitiza um DataFrame agrupando linhas com base em entradas maiúsculas em uma coluna especificada.

        :param nome_coluna: O nome da coluna para verificar cabeçalhos de grupo em maiúsculas.
        :param coluna_grupo: O nome da nova coluna de grupo a ser adicionada.
        :return: DataFrame pandas sanitizado.
        """
        self.df = self.df.copy()
        # Inicializa a coluna de grupo
        self.df[coluna_grupo] = None
        # Remove espaços em branco
        self.df[nome_coluna] = self.df[nome_coluna].str.strip()
        tipo_atual = None

        for indice, linha in self.df.iterrows():
            valor = linha[nome_coluna]
            if valor.isupper():
                tipo_atual = valor
            else:
                self.df.at[indice, coluna_grupo] = tipo_atual

        # Filtra as linhas onde o valor da coluna não está em maiúsculas
        df_sanitizado = self.df[~self.df[nome_coluna].str.isupper()]
        # Reseta o índice e insere a coluna 'id'
        df_sanitizado = df_sanitizado.reset_index(drop=True)
        df_sanitizado.insert(0, 'id', df_sanitizado.index + 1)
        return df_sanitizado

    def _sanitizar_importacao_exportacao(self):
        """
        Sanitiza datasets de Importação e Exportação transformando-os em formato longo.
        """
        try:
            registros = []

            # Obter a lista de anos a partir das colunas
            colunas = self.df.columns
            colunas_anos = [col for col in colunas if col.startswith(('19', '20')) and not col.endswith('.1')]

            for _, linha in self.df.iterrows():
                pais = linha['País']
                for coluna_ano in colunas_anos:
                    ano = int(coluna_ano)
                    quantidade = linha.get(coluna_ano, None)
                    valor = linha.get(f"{coluna_ano}.1", None)

                    if pd.notnull(quantidade) and pd.notnull(valor):
                        registros.append({
                            "País": pais,
                            "ano": ano,
                            "quantidade": quantidade,
                            "valor_usd": valor
                        })

            df_sanitizado = pd.DataFrame(registros)
            self.df = df_sanitizado
        except KeyError as e:
            logger.error(f"Erro: coluna não encontrada. Verifique se a coluna 'País' ou as colunas de anos estão corretas: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro durante a sanitização de 'Importacao/Exportacao': {e}")
            raise


def main():
    # Configuração dos datasets
    datasets = {
        'producao': {
            'url': 'http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv',
            'columns_to_drop': ['control', 'id'],
            'nome_coluna': 'produto',
            'coluna_grupo': 'Tipo',
            'delimitador': ';',
            'codificacao': 'utf-8',
            'special_processing': None
        },
        'processamento': {
            'url': 'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv',
            'columns_to_drop': ['control', 'id'],
            'nome_coluna': 'cultivar',
            'coluna_grupo': 'Tipo',
            'delimitador': ';',
            'codificacao': 'utf-8',
            'special_processing': None
        },
        'comercio': {
            'url': 'http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv',
            'columns_to_drop': ['control', 'id'],
            'nome_coluna': 'Produto',
            'coluna_grupo': 'Tipo',
            'delimitador': ';',
            'codificacao': 'utf-8',
            'special_processing': 'comercio_outros_vinhos'
        },
        'importacao': {
            'url': 'http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv',
            'columns_to_drop': [],
            'nome_coluna': None,
            'coluna_grupo': None,
            'delimitador': ';',
            'codificacao': 'utf-8',
            'special_processing': 'importacao_exportacao'
        },
        'exportacao': {
            'url': 'http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv',
            'columns_to_drop': [],
            'nome_coluna': None,
            'coluna_grupo': None,
            'delimitador': ';',
            'codificacao': 'utf-8',
            'special_processing': 'importacao_exportacao'
        }
    }

    # Definir o caminho onde os dados serão salvos
    caminho_saida = './techchallenge/vitivinicultura/data/'

    for chave, config in datasets.items():
        config['caminho_saida'] = caminho_saida
        try:
            logger.info(f"\nIniciando processamento para: {chave}")
            sanitizador = SanitizadorDataset(config)
            sanitizador.baixar_e_carregar_csv()
            df_sanitizado = sanitizador.sanitizar()
            sanitizador.salvar_csv(df_sanitizado, f'{chave}_sanitizado.csv')
            sanitizador.salvar_json(df_sanitizado, f'{chave}_sanitizado.json')
        except Exception as e:
            logger.error(f"Erro ao processar {chave}: {e}")


if __name__ == "__main__":
    main()

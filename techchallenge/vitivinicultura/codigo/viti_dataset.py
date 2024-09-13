import os
import json
import requests
import pandas as pd
from io import StringIO
import logging
from typing import Dict, Any

# Configurar o logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SanitizadorDataset:
    def __init__(self, url: str, caminho_saida: str, delimitador: str = ';', codificacao: str = 'utf-8'):
        """
        Classe base para sanitização de datasets.

        :param url: URL para download do dataset.
        :param caminho_saida: Diretório local para salvar o dataset sanitizado.
        :param delimitador: Delimitador usado no arquivo CSV.
        :param codificacao: Codificação do arquivo CSV.
        """
        self.url = url
        self.caminho_saida = caminho_saida
        self.delimitador = delimitador
        self.codificacao = codificacao
        self.df = None

    def baixar_e_carregar_csv(self) -> None:
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

    def salvar_json(self, df_sanitizado: pd.DataFrame, nome_arquivo: str) -> None:
        """
        Salva o DataFrame sanitizado em um arquivo JSON.

        :param df_sanitizado: O DataFrame pandas sanitizado.
        :param nome_arquivo: O nome do arquivo para salvar o JSON.
        """
        try:
            caminho_saida = os.path.join(self.caminho_saida, nome_arquivo)
            dados_json = df_sanitizado.to_json(orient='records', force_ascii=False)

            with open(caminho_saida, 'w', encoding='utf-8') as f:
                f.write(dados_json)
            logger.info(f"JSON sanitizado salvo com sucesso em: {caminho_saida}")
        except Exception as e:
            logger.error(f"Erro ao salvar o arquivo JSON sanitizado: {e}")
            raise

    def salvar_dados_json(self, dados: Dict[Any, Any], nome_arquivo: str) -> None:
        """
        Salva o dicionário de dados sanitizados em um arquivo JSON.

        :param dados: Os dados sanitizados como um dicionário.
        :param nome_arquivo: O nome do arquivo para salvar o JSON.
        """
        try:
            caminho_saida = os.path.join(self.caminho_saida, nome_arquivo)
            with open(caminho_saida, 'w', encoding='utf-8') as arquivo_json:
                json.dump(dados, arquivo_json, indent=4, ensure_ascii=False)
            logger.info(f"JSON sanitizado salvo com sucesso em: {caminho_saida}")
        except Exception as e:
            logger.error(f"Erro ao salvar o arquivo JSON sanitizado: {e}")
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

        # Filtra as linhas onde o valor da coluna está em maiúsculas
        df_sanitizado = self.df[~self.df[nome_coluna].str.isupper()]
        # Reseta o índice e insere a coluna 'id'
        df_sanitizado = df_sanitizado.reset_index(drop=True)
        df_sanitizado.insert(0, 'id', df_sanitizado.index + 1)
        return df_sanitizado


class SanitizadorProducao(SanitizadorDataset):
    def sanitizar(self) -> pd.DataFrame:
        """
        Sanitiza o dataset 'Producao'.

        :return: DataFrame pandas sanitizado.
        """
        try:
            logger.info("Iniciando sanitização do arquivo 'Producao'")
            # Remove colunas desnecessárias
            self.df = self.df.drop(columns=['control', 'id'])
            # Usa o método auxiliar
            df_sanitizado = self._sanitizar_grupos_maiusculos(nome_coluna='produto', coluna_grupo='Tipo')
            logger.info("Sanitização do arquivo 'Producao' concluída")
            return df_sanitizado
        except Exception as e:
            logger.error(f"Erro durante a sanitização de 'Producao': {e}")
            raise


class SanitizadorProcessamento(SanitizadorDataset):
    def sanitizar(self) -> pd.DataFrame:
        """
        Sanitiza o dataset 'Processamento'.

        :return: DataFrame pandas sanitizado.
        """
        try:
            logger.info("Iniciando sanitização do arquivo 'Processamento'")
            # Remove colunas desnecessárias
            self.df = self.df.drop(columns=['control', 'id'])
            # Usa o método auxiliar
            df_sanitizado = self._sanitizar_grupos_maiusculos(nome_coluna='cultivar', coluna_grupo='Tipo')
            logger.info("Sanitização do arquivo 'Processamento' concluída")
            return df_sanitizado
        except Exception as e:
            logger.error(f"Erro durante a sanitização de 'Processamento': {e}")
            raise


class SanitizadorComercio(SanitizadorDataset):
    def sanitizar(self) -> pd.DataFrame:
        """
        Sanitiza o dataset 'Comercio'.

        :return: DataFrame pandas sanitizado.
        """
        try:
            logger.info("Iniciando sanitização do arquivo 'Comercio'")
            # Remove colunas desnecessárias
            self.df = self.df.drop(columns=['control', 'id'])
            # Usa o método auxiliar
            df_sanitizado = self._sanitizar_grupos_maiusculos(nome_coluna='Produto', coluna_grupo='Tipo')

            # Encontra o índice de "Outros vinhos" e define 'Tipo' como 'OUTROS' a partir desse índice
            df_sanitizado['Produto'] = df_sanitizado['Produto'].str.strip()
            indices_outros = df_sanitizado[df_sanitizado['Produto'].str.contains("Outros vinhos", case=False, na=False)].index
            if not indices_outros.empty:
                indice_inicio = indices_outros[0]
                df_sanitizado.loc[indice_inicio:, 'Tipo'] = "OUTROS"
            logger.info("Sanitização do arquivo 'Comercio' concluída")
            return df_sanitizado
        except Exception as e:
            logger.error(f"Erro durante a sanitização de 'Comercio': {e}")
            raise


class SanitizadorImportacaoExportacao(SanitizadorDataset):
    def sanitizar(self) -> Dict[str, Any]:
        """
        Sanitiza o dataset 'Importacao' ou 'Exportacao'.

        :return: Dados sanitizados como um dicionário.
        """
        try:
            logger.info("Iniciando sanitização do arquivo 'Importacao/Exportacao'")
            dados_json = {}

            # Obter a lista de anos a partir das colunas
            colunas = self.df.columns
            colunas_anos = [col for col in colunas if col.startswith(('19', '20')) and not col.endswith('.1')]

            for _, linha in self.df.iterrows():
                pais = linha['País']
                dados_pais = []

                for coluna_ano in colunas_anos:
                    ano = int(coluna_ano)
                    quantidade = linha.get(coluna_ano, None)
                    valor = linha.get(f"{coluna_ano}.1", None)

                    if pd.notnull(quantidade) and pd.notnull(valor):
                        dados_pais.append({
                            "ano": ano,
                            "quantidade": quantidade,
                            "valor_usd": valor
                        })

                if dados_pais:
                    dados_json[pais] = dados_pais

            logger.info("Sanitização do arquivo 'Importacao/Exportacao' concluída")
            return dados_json
        except KeyError as e:
            logger.error(f"Erro: coluna não encontrada. Verifique se a coluna 'País' ou as colunas de anos estão corretas: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro durante a sanitização de 'Importacao/Exportacao': {e}")
            raise


def main():
    # URLs para baixar os arquivos diretamente da internet
    urls = {
        'producao': 'http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv',
        'processamento': 'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv',
        'comercio': 'http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv',
        'importacao': 'http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv',
        'exportacao': 'http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv'
    }

    # Definir o caminho onde os dados serão salvos
    caminho_saida = './techchallenge/vitivinicultura/data/'

    # Instanciação e execução
    sanitizadores = {
        'producao': SanitizadorProducao(urls['producao'], caminho_saida),
        'processamento': SanitizadorProcessamento(urls['processamento'], caminho_saida),
        'comercio': SanitizadorComercio(urls['comercio'], caminho_saida),
        'importacao': SanitizadorImportacaoExportacao(urls['importacao'], caminho_saida),
        'exportacao': SanitizadorImportacaoExportacao(urls['exportacao'], caminho_saida),
    }

    # Sanitização e salvamento dos dados
    for chave, sanitizador in sanitizadores.items():
        try:
            logger.info(f"\nIniciando processamento para: {chave}")
            sanitizador.baixar_e_carregar_csv()

            if chave in ['producao', 'processamento', 'comercio']:
                df_sanitizado = sanitizador.sanitizar()
                sanitizador.salvar_csv(df_sanitizado, f'{chave}_sanitizado.csv')
                sanitizador.salvar_json(df_sanitizado, f'{chave}_sanitizado.json')
            else:  # 'importacao' e 'exportacao'
                dados_json = sanitizador.sanitizar()
                sanitizador.salvar_dados_json(dados_json, f'{chave}_sanitizado.json')
        except Exception as e:
            logger.error(f"Erro ao processar {chave}: {e}")


if __name__ == "__main__":
    main()

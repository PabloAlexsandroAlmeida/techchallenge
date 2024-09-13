import pandas as pd
import json
import requests
from io import StringIO
import logging
from typing import Optional, Dict, Any, List

# Configuração do logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class DatasetSanitizer:
    """
    Classe base para manipulação de sanitização de datasets. Baixa um arquivo CSV de uma URL,
    processa e fornece métodos para salvar em diferentes formatos.
    """

    def __init__(self, url: str, delimiter: str = ';', encoding: str = 'utf-8'):
        self.url = url  # URL do arquivo CSV a ser baixado
        self.delimiter = delimiter  # Delimitador do CSV, por padrão é ponto e vírgula
        self.encoding = encoding  # Codificação do arquivo, por padrão UTF-8
        self.df: Optional[pd.DataFrame] = None  # DataFrame onde o CSV será armazenado após o download

    def download_and_load_csv(self) -> None:
        """
        Baixa o CSV da URL fornecida e carrega em um DataFrame pandas.
        """
        try:
            logging.info(f"Baixando arquivo de: {self.url}")
            response = requests.get(self.url)
            response.raise_for_status()

            # Salva o conteúdo original em um arquivo local
            original_output_path = self.url.split("/")[-1]
            with open(original_output_path, 'wb') as f:
                f.write(response.content)
            logging.info(f"Arquivo original salvo com sucesso em: {original_output_path}")

            # Decodifica o conteúdo e carrega no DataFrame
            csv_data = response.content.decode(self.encoding)
            self.df = pd.read_csv(StringIO(csv_data), delimiter=self.delimiter)
            logging.info(f"Arquivo baixado e carregado com sucesso: {self.url}")

        except Exception as e:
            logging.error(f"Erro ao baixar ou carregar o arquivo de {self.url}: {e}")
            raise

    def save_csv(self, df_clean: pd.DataFrame, output_path: str) -> None:
        """
        Salva o DataFrame limpo em um arquivo CSV.
        """
        try:
            df_clean.to_csv(output_path, index=False)
            logging.info(f"CSV sanitizado salvo com sucesso em: {output_path}")
        except Exception as e:
            logging.error(f"Erro ao salvar o arquivo CSV sanitizado: {e}")
            raise

    def save_json(self, df_clean: pd.DataFrame, output_path: str) -> None:
        """
        Salva o DataFrame limpo em um arquivo JSON.
        """
        try:
            # Remova 'lines=True' da chamada
            json_data = df_clean.to_json(orient='records', force_ascii=False)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_data)
            logging.info(f"JSON sanitizado salvo com sucesso em: {output_path}")
        except Exception as e:
            logging.error(f"Erro ao salvar o arquivo JSON sanitizado: {e}")
            raise



class ProducaoSanitizer(DatasetSanitizer):
    def sanitize(self) -> pd.DataFrame:
        """
        Sanitiza o dataset de 'Produção'.
        """
        try:
            logging.info("Iniciando sanitização do arquivo de 'Produção'")
            # Remove colunas desnecessárias
            self.df = self.df.drop(columns=['control', 'id'])
            self.df['Tipo'] = None  # Cria a coluna 'Tipo'
            self.df['produto'] = self.df['produto'].str.strip()  # Remove espaços em branco de 'produto'

            # Identifica tipos e atribui
            mask_upper = self.df['produto'].str.isupper()
            self.df.loc[mask_upper, 'Tipo'] = self.df.loc[mask_upper, 'produto']
            self.df['Tipo'] = self.df['Tipo'].ffill()

            # Remove linhas que são apenas nomes de tipos
            df_clean = self.df[~mask_upper].copy()
            # Adiciona uma coluna 'id' incremental
            df_clean.insert(0, 'id', range(1, len(df_clean) + 1))
            logging.info("Sanitização do arquivo de 'Produção' concluída")
            return df_clean

        except Exception as e:
            logging.error(f"Erro durante a sanitização de 'Produção': {e}")
            raise


class ProcessamentoSanitizer(DatasetSanitizer):
    def sanitize(self) -> pd.DataFrame:
        """
        Sanitiza o dataset de 'Processamento'.
        """
        try:
            logging.info("Iniciando sanitização do arquivo de 'Processamento'")
            # Remove colunas desnecessárias
            self.df = self.df.drop(columns=['control', 'id'])
            self.df['Tipo'] = None  # Cria a coluna 'Tipo'
            self.df['cultivar'] = self.df['cultivar'].str.strip()  # Remove espaços em branco de 'cultivar'

            # Identifica tipos e atribui
            mask_upper = self.df['cultivar'].str.isupper()
            self.df.loc[mask_upper, 'Tipo'] = self.df.loc[mask_upper, 'cultivar']
            self.df['Tipo'] = self.df['Tipo'].ffill()

            # Remove linhas que são apenas nomes de tipos
            df_clean = self.df[~mask_upper].copy()
            # Adiciona uma coluna 'id' incremental
            df_clean.insert(0, 'id', range(1, len(df_clean) + 1))
            logging.info("Sanitização do arquivo de 'Processamento' concluída")
            return df_clean

        except Exception as e:
            logging.error(f"Erro durante a sanitização de 'Processamento': {e}")
            raise


class ComercioSanitizer(DatasetSanitizer):
    def sanitize(self) -> pd.DataFrame:
        """
        Sanitiza o dataset de 'Comércio'.
        """
        try:
            logging.info("Iniciando sanitização do arquivo de 'Comércio'")
            # Remove colunas desnecessárias
            self.df = self.df.drop(columns=['control', 'id'])
            self.df['Tipo'] = None  # Cria a coluna 'Tipo'
            self.df['Produto'] = self.df['Produto'].str.strip()  # Remove espaços em branco de 'Produto'

            # Identifica tipos e atribui
            mask_upper = self.df['Produto'].str.isupper()
            self.df.loc[mask_upper, 'Tipo'] = self.df.loc[mask_upper, 'Produto']
            self.df['Tipo'] = self.df['Tipo'].ffill()

            # Remove linhas que são apenas nomes de tipos
            df_clean = self.df[~mask_upper].copy()

            # Define 'Tipo' como 'OUTROS' a partir de 'Outros vinhos'
            outros_mask = df_clean['Produto'].str.contains("Outros vinhos", case=False, na=False)
            if outros_mask.any():
                outros_start_index = df_clean.loc[outros_mask].index[0]
                df_clean.loc[outros_start_index:, 'Tipo'] = "OUTROS"

            # Adiciona uma coluna 'id' incremental
            df_clean.insert(0, 'id', range(1, len(df_clean) + 1))
            logging.info("Sanitização do arquivo de 'Comércio' concluída")
            return df_clean

        except Exception as e:
            logging.error(f"Erro durante a sanitização de 'Comércio': {e}")
            raise


class ImportacaoExportacaoSanitizer(DatasetSanitizer):
    def sanitize(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Sanitiza o dataset de 'Importação' ou 'Exportação'.
        """
        try:
            logging.info("Iniciando sanitização do arquivo de 'Importação/Exportação'")
            # Identifica colunas correspondentes aos anos
            year_columns = [col for col in self.df.columns if col.isdigit()]

            data_json = {}
            for _, row in self.df.iterrows():
                pais = row['País']
                dados_pais = []

                for ano in year_columns:
                    quantidade = row.get(ano)
                    valor = row.get(f"{ano}.1")
                    if pd.notnull(quantidade) or pd.notnull(valor):
                        dados_pais.append({
                            "ano": int(ano),
                            "quantidade": quantidade,
                            "valor_usd": valor
                        })
                data_json[pais] = dados_pais

            logging.info("Sanitização do arquivo de 'Importação/Exportação' concluída")
            return data_json

        except KeyError as e:
            logging.error(f"Erro: coluna não encontrada. Verifique se a coluna 'País' ou as colunas de anos estão corretas: {e}")
            raise
        except Exception as e:
            logging.error(f"Erro durante a sanitização de 'Importação/Exportação': {e}")
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

    # Instancia as classes de sanitização com suas respectivas URLs
    sanitizers = {
        'producao': ProducaoSanitizer(urls['producao']),
        'processamento': ProcessamentoSanitizer(urls['processamento']),
        'comercio': ComercioSanitizer(urls['comercio']),
        'importacao': ImportacaoExportacaoSanitizer(urls['importacao']),
        'exportacao': ImportacaoExportacaoSanitizer(urls['exportacao']),
    }

    # Loop para processar e sanitizar cada arquivo
    for key, sanitizer in sanitizers.items():
        try:
            logging.info(f"\nIniciando processamento para: {key}")
            sanitizer.download_and_load_csv()  # Baixa e carrega o CSV

            if key in ['producao', 'processamento', 'comercio']:
                df_clean = sanitizer.sanitize()  # Sanitiza o DataFrame
                sanitizer.save_csv(df_clean, f'{key}_sanitizado.csv')  # Salva como CSV
                sanitizer.save_json(df_clean, f'{key}_sanitizado.json')  # Salva como JSON
            else:
                data_json = sanitizer.sanitize()
                output_path = f'{key}_sanitizado.json'
                with open(output_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data_json, json_file, indent=4, ensure_ascii=False)  # Salva o JSON formatado
                logging.info(f"JSON sanitizado salvo com sucesso em: {output_path}")
        except Exception as e:
            logging.error(f"Erro ao processar {key}: {e}")


if __name__ == "__main__":
    main()

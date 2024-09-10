import pandas as pd
import json
import requests
from io import StringIO

class DatasetSanitizer:
    def __init__(self, url, delimiter=';', encoding='utf-8'):
        self.url = url
        self.delimiter = delimiter
        self.encoding = encoding
        self.df = None

    def download_and_load_csv(self):
        try:
            print(f"Baixando arquivo de: {self.url}")
            response = requests.get(self.url)
            response.raise_for_status()
            
            # Salvar o arquivo original direto no disco
            original_output_path = f'{self.url.split("/")[-1]}'
            with open(original_output_path, 'wb') as f:
                f.write(response.content)
            print(f"Arquivo original salvo com sucesso em: {original_output_path}")
            
            # Decodificar o conteúdo baixado
            csv_data = response.content.decode(self.encoding)
            
            # Carregar o CSV usando a string decodificada
            self.df = pd.read_csv(StringIO(csv_data), delimiter=self.delimiter)
            print(f"Arquivo baixado e carregado com sucesso: {self.url}")
        except Exception as e:
            print(f"Erro ao baixar ou carregar o arquivo de {self.url}: {e}")
            raise

    def save_csv(self, df_clean, output_path):
        try:
            df_clean.to_csv(output_path, index=False)
            print(f"CSV sanitizado salvo com sucesso em: {output_path}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo CSV sanitizado: {e}")
            raise

    def save_json(self, df_clean, output_path):
        try:
            json_data = df_clean.to_json(orient='records', lines=True, force_ascii=False)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_data)
            print(f"JSON sanitizado salvo com sucesso em: {output_path}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo JSON sanitizado: {e}")
            raise

class ProducaoSanitizer(DatasetSanitizer):
    def sanitize(self):
        try:
            print("Iniciando sanitização do arquivo de Produção")
            self.df = self.df.drop(columns=['control', 'id'])
            self.df['Tipo'] = None
            self.df['produto'] = self.df['produto'].str.strip()
            current_type = None

            for index, row in self.df.iterrows():
                if row['produto'].isupper():
                    current_type = row['produto']
                else:
                    self.df.at[index, 'Tipo'] = current_type

            df_clean = self.df[~self.df['produto'].str.isupper()]
            df_clean.insert(0, 'id', range(1, len(df_clean) + 1))
            print("Sanitização do arquivo de Produção concluída")
            return df_clean
        except Exception as e:
            print(f"Erro durante a sanitização de Produção: {e}")
            raise

class ProcessamentoSanitizer(DatasetSanitizer):
    def sanitize(self):
        try:
            print("Iniciando sanitização do arquivo de Processamento")
            self.df = self.df.drop(columns=['control', 'id'])
            self.df['Tipo'] = None
            self.df['cultivar'] = self.df['cultivar'].str.strip()
            current_type = None

            for index, row in self.df.iterrows():
                if row['cultivar'].isupper():
                    current_type = row['cultivar']
                else:
                    self.df.at[index, 'Tipo'] = current_type

            df_clean = self.df[~self.df['cultivar'].str.isupper()]
            df_clean.insert(0, 'id', range(1, len(df_clean) + 1))
            print("Sanitização do arquivo de Processamento concluída")
            return df_clean
        except Exception as e:
            print(f"Erro durante a sanitização de Processamento: {e}")
            raise

class ComercioSanitizer(DatasetSanitizer):
    def sanitize(self):
        try:
            print("Iniciando sanitização do arquivo de Comércio")
            self.df = self.df.drop(columns=['control', 'id'])
            self.df['Tipo'] = None
            self.df['Produto'] = self.df['Produto'].str.strip()
            current_type = None

            for index, row in self.df.iterrows():
                if row['Produto'].isupper():
                    current_type = row['Produto']
                else:
                    self.df.at[index, 'Tipo'] = current_type

            df_clean = self.df[~self.df['Produto'].str.isupper()]
            outros_start_index = df_clean[df_clean['Produto'].str.contains("Outros vinhos", case=False, na=False)].index[0]
            df_clean.loc[outros_start_index:, 'Tipo'] = "OUTROS"
            df_clean.insert(0, 'id', range(1, len(df_clean) + 1))
            print("Sanitização do arquivo de Comércio concluída")
            return df_clean
        except Exception as e:
            print(f"Erro durante a sanitização de Comércio: {e}")
            raise

class ImportacaoExportacaoSanitizer(DatasetSanitizer):
    def sanitize(self):
        try:
            print("Iniciando sanitização do arquivo de Importação/Exportação")
            data_json = {}
            for _, row in self.df.iterrows():
                country = row['País']
                data_json[country] = []

                for year in range(1970, 2024):
                    year_str = str(year)
                    quantity = row[year_str] if year_str in self.df.columns else None
                    value = row[f"{year_str}.1"] if f"{year_str}.1" in self.df.columns else None

                    if quantity is not None and value is not None:
                        data_json[country].append({
                            "ano": year,
                            "quantidade": quantity,
                            "valor_usd": value
                        })
            print("Sanitização do arquivo de Importação/Exportação concluída")
            return data_json
        except KeyError as e:
            print(f"Erro: coluna não encontrada. Verifique se a coluna 'País' ou as colunas de anos estão corretas: {e}")
            raise
        except Exception as e:
            print(f"Erro durante a sanitização de Importação/Exportação: {e}")
            raise

# URLs para baixar os arquivos diretamente da internet
urls = {
    'producao': 'http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv',
    'processamento': 'http://vitibrasil.cnpuv.embrapa.br/download/ProcessaViniferas.csv',
    'comercio': 'http://vitibrasil.cnpuv.embrapa.br/download/Comercio.csv',
    'importacao': 'http://vitibrasil.cnpuv.embrapa.br/download/ImpVinhos.csv',
    'exportacao': 'http://vitibrasil.cnpuv.embrapa.br/download/ExpVinho.csv'
}

# Instanciação e execução
sanitizers = {
    'producao': ProducaoSanitizer(urls['producao']),
    'processamento': ProcessamentoSanitizer(urls['processamento']),
    'comercio': ComercioSanitizer(urls['comercio']),
    'importacao': ImportacaoExportacaoSanitizer(urls['importacao']),
    'exportacao': ImportacaoExportacaoSanitizer(urls['exportacao']),
}

# Sanitização e salvamento dos dados
for key, sanitizer in sanitizers.items():
    try:
        print(f"\nIniciando processamento para: {key}")
        sanitizer.download_and_load_csv()

        if key in ['producao', 'processamento', 'comercio']:
            df_clean = sanitizer.sanitize()
            sanitizer.save_csv(df_clean, f'{key}_sanitizado.csv')
            sanitizer.save_json(df_clean, f'{key}_sanitizado.json')
        else:  # importacao/exportacao
            data_json = sanitizer.sanitize()
            with open(f'{key}_sanitizado.json', 'w', encoding='utf-8') as json_file:
                json.dump(data_json, json_file, indent=4, ensure_ascii=False)
            print(f"JSON sanitizado salvo com sucesso em: {key}_sanitizado.json")
    except Exception as e:
        print(f"Erro ao processar {key}: {e}")

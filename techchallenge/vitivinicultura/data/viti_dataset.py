import pandas as pd
import json
import requests
from io import StringIO

# Classe principal que lida com a sanitização de datasets. 
# Baixa o CSV de uma URL, faz o tratamento e oferece métodos para salvar em diferentes formatos.
class DatasetSanitizer:
    def __init__(self, url, delimiter=';', encoding='utf-8'):
        self.url = url  # URL do arquivo CSV a ser baixado
        self.delimiter = delimiter  # Delimitador do CSV, por padrão é ponto e vírgula
        self.encoding = encoding  # Codificação do arquivo, por padrão UTF-8
        self.df = None  # DataFrame onde o CSV será armazenado após o download

    # Método para baixar o CSV do site da Embrapa e carregar em um DataFrame pandas
    def download_and_load_csv(self):
        try:
            print(f"Baixando arquivo de: {self.url}")
            response = requests.get(self.url)  # Baixa o conteúdo do CSV
            response.raise_for_status()  # Verifica se o download foi bem-sucedido
            
            # Salva o conteúdo original baixado em um arquivo local
            original_output_path = f'{self.url.split("/")[-1]}'  # Nome do arquivo original
            with open(original_output_path, 'wb') as f:
                f.write(response.content)  # Salva o conteúdo binário
            print(f"Arquivo original salvo com sucesso em: {original_output_path}")
            
            # Decodifica o conteúdo para string usando a codificação especificada
            csv_data = response.content.decode(self.encoding)
            
            # Carrega o CSV para o DataFrame pandas
            self.df = pd.read_csv(StringIO(csv_data), delimiter=self.delimiter)
            print(f"Arquivo baixado e carregado com sucesso: {self.url}")
        except Exception as e:
            print(f"Erro ao baixar ou carregar o arquivo de {self.url}: {e}")
            raise

    # Método para salvar o DataFrame limpo em CSV
    def save_csv(self, df_clean, output_path):
        try:
            df_clean.to_csv(output_path, index=False)  # Salva o DataFrame sem o índice
            print(f"CSV sanitizado salvo com sucesso em: {output_path}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo CSV sanitizado: {e}")
            raise

    # Método para salvar o DataFrame limpo em JSON
    def save_json(self, df_clean, output_path):
        try:
            json_data = df_clean.to_json(orient='records', lines=True, force_ascii=False)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_data)  # Salva o JSON em formato legível
            print(f"JSON sanitizado salvo com sucesso em: {output_path}")
        except Exception as e:
            print(f"Erro ao salvar o arquivo JSON sanitizado: {e}")
            raise

# Classe específica para sanitização do arquivo de Produção
class ProducaoSanitizer(DatasetSanitizer):
    def sanitize(self):
        try:
            print("Iniciando sanitização do arquivo de Produção")
            # Remove as colunas desnecessárias
            self.df = self.df.drop(columns=['control', 'id'])
            self.df['Tipo'] = None  # Cria nova coluna 'Tipo'
            self.df['produto'] = self.df['produto'].str.strip()  # Remove espaços em branco dos produtos
            current_type = None  # Variável para armazenar o tipo atual

            # Itera sobre cada linha do DataFrame para identificar os tipos de produtos
            for index, row in self.df.iterrows():
                if row['produto'].isupper():  # Se o nome do produto está em maiúsculas, é um tipo
                    current_type = row['produto']
                else:
                    self.df.at[index, 'Tipo'] = current_type  # Define o tipo nas linhas subsequentes

            # Filtra o DataFrame para remover as linhas que são apenas o nome do tipo
            df_clean = self.df[~self.df['produto'].str.isupper()]
            # Adiciona uma coluna de ID incremental
            df_clean.insert(0, 'id', range(1, len(df_clean) + 1))
            print("Sanitização do arquivo de Produção concluída")
            return df_clean
        except Exception as e:
            print(f"Erro durante a sanitização de Produção: {e}")
            raise

# Classe específica para sanitização do arquivo de Processamento
class ProcessamentoSanitizer(DatasetSanitizer):
    def sanitize(self):
        try:
            print("Iniciando sanitização do arquivo de Processamento")
            # Remove colunas desnecessárias
            self.df = self.df.drop(columns=['control', 'id'])
            self.df['Tipo'] = None  # Cria nova coluna 'Tipo'
            self.df['cultivar'] = self.df['cultivar'].str.strip()  # Remove espaços em branco da coluna cultivar
            current_type = None

            # Itera pelas linhas para identificar o tipo de cultivar
            for index, row in self.df.iterrows():
                if row['cultivar'].isupper():  # Cultivar em maiúsculas indica um novo tipo
                    current_type = row['cultivar']
                else:
                    self.df.at[index, 'Tipo'] = current_type  # Atribui o tipo corrente às linhas subsequentes

            # Remove linhas que têm apenas o nome do tipo
            df_clean = self.df[~self.df['cultivar'].str.isupper()]
            # Adiciona uma coluna de ID incremental
            df_clean.insert(0, 'id', range(1, len(df_clean) + 1))
            print("Sanitização do arquivo de Processamento concluída")
            return df_clean
        except Exception as e:
            print(f"Erro durante a sanitização de Processamento: {e}")
            raise

# Classe específica para sanitização do arquivo de Comércio
class ComercioSanitizer(DatasetSanitizer):
    def sanitize(self):
        try:
            print("Iniciando sanitização do arquivo de Comércio")
            # Remove colunas desnecessárias
            self.df = self.df.drop(columns=['control', 'id'])
            self.df['Tipo'] = None  # Cria nova coluna 'Tipo'
            self.df['Produto'] = self.df['Produto'].str.strip()  # Remove espaços em branco dos produtos
            current_type = None

            # Itera pelas linhas para identificar o tipo de produto
            for index, row in self.df.iterrows():
                if row['Produto'].isupper():  # Produto em maiúsculas indica um tipo
                    current_type = row['Produto']
                else:
                    self.df.at[index, 'Tipo'] = current_type  # Atribui o tipo corrente

            # Remove as linhas que são apenas o nome do tipo
            df_clean = self.df[~self.df['Produto'].str.isupper()]
            # A partir da linha que contém "Outros vinhos", define o tipo como "OUTROS"
            outros_start_index = df_clean[df_clean['Produto'].str.contains("Outros vinhos", case=False, na=False)].index[0]
            df_clean.loc[outros_start_index:, 'Tipo'] = "OUTROS"
            # Adiciona uma coluna de ID incremental
            df_clean.insert(0, 'id', range(1, len(df_clean) + 1))
            print("Sanitização do arquivo de Comércio concluída")
            return df_clean
        except Exception as e:
            print(f"Erro durante a sanitização de Comércio: {e}")
            raise

# Classe específica para sanitização dos arquivos de Importação e Exportação
class ImportacaoExportacaoSanitizer(DatasetSanitizer):
    def sanitize(self):
        try:
            print("Iniciando sanitização do arquivo de Importação/Exportação")
            data_json = {}  # Dicionário para armazenar os dados sanitizados
            # Itera por cada linha do DataFrame
            for _, row in self.df.iterrows():
                country = row['País']  # Obtém o país da linha atual
                data_json[country] = []  # Cria uma lista para armazenar os dados desse país

                # Itera por cada ano de 1970 a 2023, se as colunas existirem
                for year in range(1970, 2024):
                    year_str = str(year)
                    quantity = row[year_str] if year_str in self.df.columns else None
                    value = row[f"{year_str}.1"] if f"{year_str}.1" in self.df.columns else None

                    # Se quantidade e valor existirem, adiciona ao dicionário
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
        print(f"\nIniciando processamento para: {key}")
        sanitizer.download_and_load_csv()  # Baixa e carrega o CSV

        if key in ['producao', 'processamento', 'comercio']:
            df_clean = sanitizer.sanitize()  # Sanitiza o DataFrame
            sanitizer.save_csv(df_clean, f'{key}_sanitizado.csv')  # Salva como CSV
            sanitizer.save_json(df_clean, f'{key}_sanitizado.json')  # Salva como JSON
        else:  # Para importação/exportação, salva apenas como JSON
            data_json = sanitizer.sanitize()
            with open(f'{key}_sanitizado.json', 'w', encoding='utf-8') as json_file:
                json.dump(data_json, json_file, indent=4, ensure_ascii=False)  # Salva o JSON formatado
            print(f"JSON sanitizado salvo com sucesso em: {key}_sanitizado.json")
    except Exception as e:
        print(f"Erro ao processar {key}: {e}")

import pandas as pd
import json

# Carregar o dataset
file_path = 'ExpVinho.csv'
df = pd.read_csv(file_path, sep=';')

# Criar a estrutura de dicionário para conversão em JSON
data_json = {}

for _, row in df.iterrows():
    country = row['País']
    data_json[country] = []
    
    # Loop através dos anos e suas respectivas colunas de quantidade e valor
    for year in range(1970, 2024):  # De 1970 a 2023
        year_str = str(year)
        quantity = row[year_str] if year_str in df.columns else None
        value = row[f"{year_str}.1"] if f"{year_str}.1" in df.columns else None
        
        if quantity is not None and value is not None:
            data_json[country].append({
                "ano": year,
                "quantidade": quantity,
                "valor_usd": value
            })

# Converter para formato JSON com suporte a caracteres especiais
json_data = json.dumps(data_json, indent=4, ensure_ascii=False)

# Salvar o arquivo JSON
output_path = 'ExpVinho_sanitizado.json'
with open(output_path, 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

print(f'Arquivo JSON salvo em: {output_path}')

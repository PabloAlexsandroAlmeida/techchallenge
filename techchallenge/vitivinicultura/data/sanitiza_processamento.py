import pandas as pd

# Caminho do dataset
file_path = 'ProcessaViniferas.csv'

# Carregar o dataset
df = pd.read_csv(file_path, delimiter=';')

# Remover as colunas 'control' e 'id'
df = df.drop(columns=['control', 'id'])

# Criar uma nova coluna "Tipo"
df['Tipo'] = None

# Remover espaços em branco extras dos nomes dos produtos
df['cultivar'] = df['cultivar'].str.strip()

# Variável auxiliar para armazenar o tipo atual
current_type = None

# Iterar sobre as linhas do dataframe
for index, row in df.iterrows():
    # Se a linha é uma linha de Tipo (tudo em maiúsculas), atualizar o current_type
    if row['cultivar'].isupper():
        current_type = row['cultivar']
    else:
        # Para as outras linhas, atribuir o current_type
        df.at[index, 'Tipo'] = current_type

# Filtrar as linhas que são produtos (não são linhas de tipo)
df_clean = df[~df['cultivar'].str.isupper()]

# Adicionar um novo 'id' sequencial em df_clean (não df)
df_clean.insert(0, 'id', range(1, len(df_clean) + 1))

# Salvar o resultado em um novo arquivo CSV
df_clean.to_csv('ProcessaViniferas_sanitizado.csv', index=False)

print("Processamento concluído! O arquivo sanitizado foi salvo como 'ProcessaViniferas_sanitizado.csv'.")

# Converter o DataFrame para JSON
json_data = df_clean.to_json(orient='records', lines=True, force_ascii=False)

# Salvar o resultado em um arquivo JSON
output_json_path = 'ProcessaViniferas_sanitizado.json'
with open(output_json_path, 'w', encoding='utf-8') as f:
    f.write(json_data)

print(f"Arquivo JSON salvo em: {output_json_path}")
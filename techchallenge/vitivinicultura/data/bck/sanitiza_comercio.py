import pandas as pd

# Caminho do dataset
file_path = 'Comercio.csv'

# Carregar o dataset
df = pd.read_csv(file_path, delimiter=';')

# Remover as colunas 'control' e 'id'
df = df.drop(columns=['control', 'id'])

# Criar uma nova coluna "Tipo"
df['Tipo'] = None

# Remover espaços em branco extras dos nomes dos produtos
df['Produto'] = df['Produto'].str.strip()

# Variável auxiliar para armazenar o tipo atual
current_type = None

# Iterar sobre as linhas do dataframe
for index, row in df.iterrows():
    # Se a linha é uma linha de Tipo (tudo em maiúsculas), atualizar o current_type
    if row['Produto'].isupper():
        current_type = row['Produto']
    else:
        # Para as outras linhas, atribuir o current_type
        df.at[index, 'Tipo'] = current_type

# Filtrar as linhas que são produtos (não são linhas de tipo)
df_clean = df[~df['Produto'].str.isupper()]

# Identificar onde a seção "Outros" começa (linha com a palavra "Outros vinhos")
outros_start_index = df_clean[df_clean['Produto'].str.contains("Outros vinhos", case=False, na=False)].index[0]

# Atribuir "Outros" como tipo para todos os produtos a partir da linha onde "Outros vinhos" começa
df_clean.loc[outros_start_index:, 'Tipo'] = "OUTROS"

# Adicionar um novo 'id' sequencial em df_clean (não df)
df_clean.insert(0, 'id', range(1, len(df_clean) + 1))

# Salvar o resultado em um novo arquivo CSV
df_clean.to_csv('Comercio_sanitizado.csv', index=False)

print("Processamento concluído! O arquivo sanitizado foi salvo como 'Comercio_sanitizado.csv'.")

# Converter o DataFrame para JSON
json_data = df_clean.to_json(orient='records', lines=True, force_ascii=False)

# Salvar o resultado em um arquivo JSON
output_json_path = 'Comercio_sanitizado.json'
with open(output_json_path, 'w', encoding='utf-8') as f:
    f.write(json_data)

print(f"Arquivo JSON salvo em: {output_json_path}")
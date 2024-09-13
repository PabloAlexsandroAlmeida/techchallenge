# Importando as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurando o estilo dos gráficos
sns.set(style="whitegrid")

# Carregando o arquivo JSON
data = pd.read_json('comercio_sanitizado.json')

# Exibindo as primeiras linhas do DataFrame para verificar a estrutura
print(data.head())

# Transformando os dados de formato wide para long
# Isso facilita a manipulação e plotagem dos dados ao longo dos anos
data_long = pd.melt(
    data,
    id_vars=['id', 'Produto', 'Tipo'],
    var_name='Ano',
    value_name='Quantidade'
)

# Convertendo a coluna 'Ano' para inteiro
data_long['Ano'] = data_long['Ano'].astype(int)

# Exibindo as primeiras linhas do DataFrame transformado
print(data_long.head())

# ---------------------------------------
# Análise Exploratória de Dados (EDA)
# ---------------------------------------

# 1. Quantidade total produzida por ano
total_por_ano = data_long.groupby('Ano')['Quantidade'].sum().reset_index()

plt.figure(figsize=(14, 7))
sns.lineplot(data=total_por_ano, x='Ano', y='Quantidade', marker='o')
plt.title('Quantidade Total Produzida por Ano')
plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.show()

# 2. Produção por Tipo de Vinho ao longo dos anos
plt.figure(figsize=(14, 7))
sns.lineplot(data=data_long, x='Ano', y='Quantidade', hue='Tipo', estimator='sum')
plt.title('Produção por Tipo de Vinho ao Longo dos Anos')
plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.legend(title='Tipo de Vinho')
plt.show()

# 3. Produção de cada Produto específico ao longo dos anos
plt.figure(figsize=(14, 7))
sns.lineplot(data=data_long, x='Ano', y='Quantidade', hue='Produto', estimator='sum')
plt.title('Produção por Produto ao Longo dos Anos')
plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.legend(title='Produto', bbox_to_anchor=(1.05, 1), loc=2)
plt.show()

# 4. Top 5 Produtos com maior produção total
total_por_produto = data_long.groupby('Produto')['Quantidade'].sum().reset_index()
top5_produtos = total_por_produto.sort_values('Quantidade', ascending=False).head(5)

plt.figure(figsize=(10, 6))
sns.barplot(data=top5_produtos, x='Quantidade', y='Produto', palette='viridis')
plt.title('Top 5 Produtos com Maior Produção Total')
plt.xlabel('Quantidade Total')
plt.ylabel('Produto')
plt.show()

# 5. Distribuição da produção por Tipo de Vinho
plt.figure(figsize=(8, 6))
sns.boxplot(data=data_long, x='Tipo', y='Quantidade')
plt.title('Distribuição da Produção por Tipo de Vinho')
plt.xlabel('Tipo de Vinho')
plt.ylabel('Quantidade')
plt.show()

# 6. Heatmap da produção ao longo dos anos por Tipo de Vinho
pivot_data = data_long.pivot_table(values='Quantidade', index='Ano', columns='Tipo', aggfunc='sum')

plt.figure(figsize=(12, 8))
sns.heatmap(pivot_data, cmap='YlGnBu', linecolor='white', linewidths=0.1)
plt.title('Heatmap da Produção por Tipo de Vinho ao Longo dos Anos')
plt.xlabel('Tipo de Vinho')
plt.ylabel('Ano')
plt.show()

# 7. Analisando tendências específicas (Exemplo: Vinho Tinto)
vinho_tinto = data_long[data_long['Produto'] == 'Tinto']

plt.figure(figsize=(14, 7))
sns.lineplot(data=vinho_tinto, x='Ano', y='Quantidade', hue='Tipo', marker='o')
plt.title('Produção do Vinho Tinto ao Longo dos Anos por Tipo')
plt.xlabel('Ano')
plt.ylabel('Quantidade')
plt.legend(title='Tipo de Vinho')
plt.show()

# ---------------------------------------
# Observações e Insights
# ---------------------------------------
# Em 2019 houve um grande aumento na produção de vinhos em geral, somando todos os tipos.
# O motivo parece ser porque apenas a partir de 2019 os sucos de uva começaram a ser contabilizados no dataset.

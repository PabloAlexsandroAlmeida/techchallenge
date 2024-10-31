
# Vitivinicultura Data API v1

Este projeto é uma aplicação web construída com Django e Django REST Framework que fornece uma API para acessar dados relacionados à vitivinicultura no Brasil. Os dados incluem informações sobre produção, comércio, processamento, importação e exportação de produtos vitivinícolas.

## Sumário

- Visão Geral
- Pré-requisitos
- Instalação
- Configuração
- Execução
- Estrutura do Projeto
- Uso da API
- Testes
- Contribuição
- Licença
- Contato
- Agradecimentos
- Notas Adicionais

## Visão Geral

A aplicação permite:

- Baixar e sanitizar datasets de fontes externas (http://vitibrasil.cnpuv.embrapa.br/).
- Importar dados sanitizados para o banco de dados.
- Fornecer endpoints RESTful para acesso aos dados.
- Filtrar, pesquisar e ordenar dados através da API.

Os dados são obtidos de fontes públicas e processados para serem consumidos por aplicações clientes, pesquisadores e entusiastas da área de vitivinicultura.

## Pré-requisitos

Antes de iniciar, certifique-se de ter instalado em seu ambiente:

- Python 3.11.2 ou superior
- pip (gerenciador de pacotes do Python) 24.2 ou superior
- Todos os pacotes listados em `requirements.txt`

## Instalação

1. **Clone o repositório**

   ```bash
   git clone https://github.com/PabloAlexsandroAlmeida/techchallenge.git
   cd vitivinicultura-api
   ```

2. **Crie e ative um ambiente virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate # No Windows, use venv\Scripts\activate
   ```

3. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

## Configuração

### Migrações do Banco de Dados

Execute as migrações para criar as tabelas no banco de dados.

```bash
python manage.py migrate
```

## Execução

### Baixar e Sanitizar os Datasets

Execute o comando customizado para baixar e sanitizar os datasets iniciais.

```bash
python manage.py dataset_stage1
```

### Importar Dados para o Banco de Dados

Execute o comando customizado para importar os dados sanitizados para o banco de dados.

```bash
python manage.py dataset_stage2
```

### Iniciar o Servidor de Desenvolvimento

Inicie o servidor do Django.

```bash
python manage.py runserver
```

A aplicação estará disponível em `http://localhost:8000/`.

## Estrutura do Projeto

Abaixo está uma visão geral dos principais arquivos e diretórios do projeto:

```
vitivinicultura/
    models.py: Define os modelos de dados para a aplicação, incluindo Producao, Comercio, Processamento, Exportacao, Importacao, AnoValor e Pais.
    serializers.py: Define os serializers para converter os modelos em formatos JSON para a API.
    views.py: Contém os ViewSets para os modelos, fornecendo endpoints RESTful.
    urls.py: Configura as rotas da API utilizando roteadores do Django REST Framework.
    data/: Diretório onde os datasets brutos e sanitizados são armazenados.
    management/commands/
        dataset_stage1.py: Script para baixar e sanitizar os datasets iniciais.
        dataset_stage2.py: Script para importar os dados sanitizados para o banco de dados.
```

## Uso da API

A API fornece endpoints para acessar os dados de vitivinicultura. Alguns dos endpoints disponíveis incluem:

- **Produção**
    - `GET /producao/`: Lista todas as produções.
    - `GET /producao/{id}/`: Detalhes de uma produção específica.
    - Filtros disponíveis: produto, tipo.

- **Comércio**
    - `GET /comercio/`: Lista todas as informações de comércio.
    - `GET /comercio/{id}/`: Detalhes de um comércio específico.
    - Filtros disponíveis: produto, tipo.

- **Processamento**
    - `GET /processamento/`: Lista todos os processamentos.
    - `GET /processamento/{id}/`: Detalhes de um processamento específico.
    - Filtros disponíveis: produto, tipo.

- **Exportação**
    - `GET /exportacao/`: Lista todas as exportações.
    - `GET /exportacao/{id}/`: Detalhes de uma exportação específica.
    - Filtros disponíveis: pais__nome.

- **Importação**
    - `GET /importacao/`: Lista todas as importações.
    - `GET /importacao/{id}/`: Detalhes de uma importação específica.
    - Filtros disponíveis: pais__nome.

- **Ano e Valor**
    - `GET /anovalor/`: Lista todos os registros de ano e valor.
    - `GET /anovalor/{id}/`: Detalhes de um registro específico.
    - Filtros disponíveis: ano, valor, tipo_valor, além de campos relacionados.

### Exemplo de Requisição

Para filtrar produções por produto e tipo:

```bash
GET /producao/?produto=Vinho&tipo=Tinto
```

## Testes

### Executar Testes Automatizados

Se houver testes configurados, você pode executá-los com:

```bash
python manage.py test
```

## Contribuição

Contribuições são bem-vindas! Siga os passos abaixo para contribuir:

1. **Faça um Fork do Repositório**  
   Crie um fork do projeto no GitHub.

2. **Crie uma Branch para sua Feature ou Correção de Bug**

   ```bash
   git checkout -b minha-feature
   ```

3. **Commit suas Alterações**

   ```bash
   git commit -m "Minha nova feature"
   ```

4. **Envie para o Repositório Remoto**

   ```bash
   git push origin minha-feature
   ```

5. **Abra um Pull Request**  
   Descreva as mudanças propostas e aguarde a revisão.

## Licença

Este projeto está licenciado sob a MIT License.

## Agradecimentos

Agradecemos aos professores da FIAP e às fontes de dados públicas que tornaram este projeto possível.

## Notas Adicionais

- **Segurança**: Lembre-se de configurar adequadamente as chaves secretas e outras configurações de segurança antes de implantar em produção.
- **Atualizações**: Verifique regularmente se há atualizações nas fontes de dados para manter o banco de dados atualizado.

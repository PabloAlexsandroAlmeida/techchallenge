import requests
import base64
import io
import pandas as pd
import boto3
from datetime import datetime

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # URL para download
    url = f'https://sistemaswebb3-listados.b3.com.br/indexProxy/indexCall/GetDownloadPortfolioDay/eyJpbmRleCI6IklCT1YiLCJsYW5ndWFnZSI6InB0LWJyIn0='

    # Iniciar o download
    response = requests.get(url)

    # Decodificar a resposta base64
    base64_data = response.text
    csv_data = base64.b64decode(base64_data).decode('iso-8859-1')

    # Preparar os dados CSV
    lines = csv_data.strip().split('\r\n')

    date_string = lines[0].split(' ')[-1]
    date_object = datetime.strptime(date_string, "%d/%m/%y")
    date = date_object.strftime("%Y-%m-%d")

    lines[1] = f'Data;Codigo;Acao;Tipo;QuantTeorica;Partic'
    lines = lines[1:-2]

    for i in range(1, len(lines)):
        lines[i] = f'{date};{lines[i][:-1]}'
        lines[i] = lines[i].replace(".", "")
        lines[i] = lines[i].replace(",", ".")

    # Criar o CSV para DataFrame
    csv_data = '\n'.join(lines)

    # Carregar os dados no DataFrame
    df = pd.read_csv(io.StringIO(csv_data), sep=';')

    # Gerar o arquivo Parquet
    parquet_file_path = f'/tmp/b3-{date}.parquet'
    df.to_parquet(parquet_file_path, index=False)

    # Enviar o arquivo Parquet para o S3
    bucket_name = '897722708429-raw'  # Substitua pelo seu nome do bucket
    s3_file_key = 'b3-portfolio.parquet'

    try:
        s3_client.upload_file(parquet_file_path, bucket_name, s3_file_key)
        print(f'Arquivo Parquet enviado para S3: {s3_file_key}')
        return {
            'statusCode': 200,
            'body': f'Arquivo enviado para o S3: {s3_file_key}'
        }
    except Exception as e:
        print(f'Erro ao enviar para S3: {e}')
        return {
            'statusCode': 500,
            'body': 'Erro ao enviar para o S3'
        }

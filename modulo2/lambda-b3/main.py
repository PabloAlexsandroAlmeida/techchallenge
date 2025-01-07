import json
import requests
import boto3
from datetime import datetime

def lambda_handler(event, context):
    # URL da API ou página com dados do Pregão B3 (substitua por fonte válida)
    url = "https://api.b3.com.br/example-endpoint"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Formatar os dados para salvar no S3
        formatted_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
        }
        
        # Nome do bucket e do arquivo
        bucket_name = "b3-data-lambda-bucket"
        file_name = f"b3_data_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"
        
        # Enviar dados para o S3
        s3_client = boto3.client("s3")
        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_name,
            Body=json.dumps(formatted_data),
            ContentType="application/json"
        )
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Data saved to S3", "file_name": file_name})
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

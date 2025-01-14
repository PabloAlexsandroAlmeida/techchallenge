import boto3
from pandas import DataFrame as pd
import yfinance as yf
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # Configurações do S3
    bucket_name = '897722708429-raw'
    s3_prefix = ''  # Prefixo opcional para organizar no S3

    # Inicializa o cliente S3
    s3 = boto3.client('s3')

    # Lista de tickers
    tickers = [
        "ALOS3", "ALPA4", "ABEV3", "ASAI3", "AURE3", "AMOB3", "AZUL4", "AZZA3",
        "B3SA3", "BBSE3", "BBDC3", "BBDC4", "BRAP4", "BBAS3", "BRKM5", "BRAV3",
        "BRFS3", "BPAC11", "CXSE3", "CRFB3", "CCRO3", "CMIG4", "COGN3", "CPLE6",
        "CSAN3", "CPFE3", "CMIN3", "CVCB3", "CYRE3", "ELET3", "ELET6", "EMBR3",
        "ENGI11", "ENEV3", "EGIE3", "EQTL3", "EZTC3", "FLRY3", "GGBR4", "GOAU4",
        "NTCO3", "HAPV3", "HYPE3", "IGTI11", "IRBR3", "ISAE4", "ITSA4", "ITUB4",
        "JBSS3", "KLBN11", "RENT3", "LREN3", "LWSA3", "MGLU3", "MRFG3", "BEEF3",
        "MRVE3", "MULT3", "PCAR3", "PETR3", "PETR4", "RECV3", "PRIO3", "PETZ3",
        "RADL3", "RAIZ4", "RDOR3", "RAIL3", "SBSP3", "SANB11", "STBP3", "SMTO3",
        "CSNA3", "SLCE3", "SUZB3", "TAEE11", "VIVT3", "TIMS3", "TOTS3", "UGPA3",
        "USIM5", "VALE3", "VAMO3", "VBBR3", "VIVA3", "WEGE3", "YDUQ3"
    ]

    # DataFrame consolidado
    consolidado = pd.DataFrame()

    # Loop através dos tickers
    hoje = datetime.now().date()
    inicio = hoje - timedelta(days=1)  # Dados do dia anterior

    for ticker in tickers:
        # Baixa os dados históricos diários
        dados = yf.download(ticker + ".SA", start=inicio, end=hoje, interval='1d')

        # Verifica se os dados foram baixados corretamente
        if not dados.empty:
            # Adiciona o ticker como uma nova coluna
            dados['Ticker'] = ticker
            consolidado = pd.concat([consolidado, dados])
            print(f"Dados do ticker {ticker} adicionados ao consolidado.")
        else:
            print(f"Não foram encontrados dados para o ticker {ticker}.")

    # Verifica se há dados para salvar
    if not consolidado.empty:
        # Define o caminho do arquivo local
        filename = f"pregrao-consolidado-{inicio}.parquet"
        file_path = f"/tmp/{filename}"

        # Salva o DataFrame consolidado como arquivo Parquet
        consolidado.to_parquet(file_path)
        print(f"Arquivo Parquet consolidado salvo localmente em '{file_path}'.")

        # Define o caminho no S3
        s3_object_name = f"{s3_prefix}{filename}"

        # Envia o arquivo para o S3
        s3.upload_file(file_path, bucket_name, s3_object_name)
        print(f"Arquivo '{file_path}' enviado para 's3://{bucket_name}/{s3_object_name}'.")
    else:
        print("Nenhum dado foi encontrado para os tickers especificados.")

    return {'result': 'Ingestao completa'}

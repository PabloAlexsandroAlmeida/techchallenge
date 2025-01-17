import boto3

def lambda_handler(event, context):
    print("lambda glue")
    glue_client = boto3.client('glue')
    response = glue_client.start_job_run(
        JobName='pos-tech'
    )

    print(response)

    return {
        'statusCode': 200,
        'body': 'Lambda Glue'
    }

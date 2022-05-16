import json
import boto3
import io
import os

CORE_LAMBDA = os.environ.get("CORE_LAMBDA")
REGION = os.environ.get("REGION")

lambda_client = boto3.client("lambda", region_name=REGION) 
s3_client = boto3.client("s3",
                        region_name= REGION,
                        aws_access_key_id = "",
                        aws_secret_access_key = "")

def lambda_handler(event, context):
    s3_data = event["Records"][0]["s3"]     
    bucket_name = s3_data["bucket"]["name"]
    file_name = s3_data["object"]["key"]
    
    parseCSV(bucket_name, file_name)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def callLambda(dni, from_date, to_date):
    payload={
        "dni":dni,
        "from_date":from_date,
        "to_date":to_date
    }
    response = lambda_client.invoke(FunctionName=CORE_LAMBDA,
                                    InvocationType="RequestResponse",
                                    Payload=payload)

    return

def parseCSV(bucket_name, file_name):
    data_stream = io.BytesIO()
    s3_client.download_fileobj(bucket_name, 
                                file_name,
                                data_stream)
    data_stream.seek(0)
    data = data_stream.read()
    rows = data.split()

    for row in rows:
        dni,from_date,to_date = row.split(",") 
        callLambda(dni, from_date, to_date)

    return
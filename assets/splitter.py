import json
import boto3
import io


lambda_client = boto3.client("lambda")
s3_client = boto3.client("s3")

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """
    bucket_name = event.Records.s3.bucket.name
    file_name = event.Records.s3.object.key
    parseCSV(bucket_name, file_name)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "hello world",
            }
        ),
    }


#def callLambda(nombre):
#    response = client.invoke(FunctionName="arn:aws:lambda:us-east-1:161142984839:function:lbas_support_resumen_cuenta",
#                             InvocationType="RequestResponse",
#                             Payload="a")
#    
#    return

def parseCSV(bucket_name, file_name):
    data_stream = io.BytesIO()
    s3_client.meta.client.download_fileobj(bucket_name, 
                                            file_name,
                                            data_stream)
    data_stream.seek(0)
    
    print("BYTESSSS")
    print(data_stream)
    
    return

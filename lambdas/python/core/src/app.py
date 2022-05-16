import json
import psycopg2
import boto3
import os
from helper import header, debits

lambda_client = boto3.client("lambda")

# Constantes
LAMBDA_PDF_CREATE = os.environment.get("LAMBDA_PDF_CREATE")
DB_NAME = os.environment.get("DB_NAME")
DB_HOST = os.environment.get("DB_HOST")
DB_USER = os.environment.get("DB_USER")
DB_PASSWORD = os.environment.get("DB_PASSWORD")

def lambda_handler(payload, context):
    success, data = connectDB(payload)
    if success:
        successcreatePDF(data)
    
    # TEST
    
    success = createPDF(data)
    print(success)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def createPDF(payload):
    # Call lambda to make PDF. Response
    response = lambda_client.invoke(FunctionName=LAMBDA_PDF_CREATE,
                                    InvocationType="RequestResponse",
                                    Payload=payload)
    
    
def connectDB(payload):
    """ 
    It connects to the database and makes a query to get the data to complete the PDF
    """
    
    conn = psycopg2.connect(database=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    # Test DB connection
    cursor = conn.cursor()
    # Queries
    header_query = header.replace(DNI=payload.get("dni"))
    cursor.execute(header)
    
    colnames = [desc[0] for desc in cursor.description]
    values = cursor.fetchall()
    data=[]

    for row in values:
        data.append(dict(zip(colnames,row)))

    debits_query = header.replace(FROM_DATE=payload.get("from_date"), TO_DATE=payload.get("to_date"), ACCOUNT_ID=account_id)
    cursor.execute(debits_query)

    success = not bool(conn.closed) # "conn.closed" return 0 it's okey.
    
    return success, data
    
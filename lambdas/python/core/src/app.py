import json
import psycopg2
import boto3
import os


lambda_client = boto3.client("lambda")

# Constantes
LAMBDA_PDF_CREATE = os.environment.get("LAMBDA_PDF_CREATE")
DB_NAME = os.environment.get("DB_NAME")
DB_HOST = os.environment.get("DB_HOST")
DB_USER = os.environment.get("DB_USER")
DB_PASSWORD = os.environment.get("DB_PASSWORD")

# Querrys
debitsANDcredits = """
SELECT t.transaction_date, t.status, t.metadata, t.amount as 'debito', 0.0 as 'credito' 
    FROM public.tb_ar_core_transactions t 
        INNER JOIN public.tb_ar_configs_params p ON p.value_2 = t.transaction_type 
        INNER JOIN public.tb_ar_gp_t1015 gp ON gp.account = t.account_from
            WHERE p.param_type = 'transaction_type' 
            AND p.value_3 = 'TRUE'
            AND t.transaction_date > '2021-11-01' 
            AND t.transaction_date <= '2021-12-01'
UNION
SELECT t.transaction_date, t.status, t.metadata, t.amount as 'credito', 0.0 as 'debito' 
    FROM public.tb_ar_core_transactions t 
        INNER JOIN public.tb_ar_configs_params p ON p.value_2 = t.transaction_type 
        INNER JOIN public.tb_ar_gp_t1015 gp ON gp.account = t.account_to
            WHERE p.param_type = 'transaction_type' 
            AND p.value_3 = 'FALSE'
            AND t.transaction_date > '{FROM_DATE}' 
            AND t.transaction_date <= '{TO_DATE}';
"""

header = """

SELECT a.account_id, concat(a.contact_first_name, ' ', a.contact_last_name) as 'titular' , a.email, c.cvu 
    FROM  public.tb_ar_cvu c INNER JOIN public.tb_ar_core_accounts a 
        ON a.account_id = c.account_id
            INNER JOIN public.tb_ar_core_users u ON u.account_id = a.account_id
            WHERE  u.cuil = {CUIL};
"""

def lambda_handler(dni, context):
    success, data = connectDB()
    if success:
        successcreatePDF(data)
    
    # TEST
    
    success = createPDF(data)
    print(success)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def createPDF(data):
    response = lambda_client.invoke(FunctionName=LAMBDA_PDF_CREATE,
                                    InvocationType="RequestResponse",
                                    Payload=data)
    
    
def connectDB():
    """ 
    It connects to the database and makes a query to get the data to complete the PDF
    """
    
    conn = psycopg2.connect(database=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    # Test DB connection
    cursor = conn.cursor()
    # Querrys
    query= "SELECT * FROM transacciones t INNER JOIN usuarios u ON t.cuenta_usuario = u.cuenta WHERE u.id = 11264993;"
    cursor.execute(query)
    
    colnames = [desc[0] for desc in cursor.description]
    values = cursor.fetchall()
    data=[]
    
    for row in values:
        data.append(dict(zip(colnames,row)))
    print(data)
    success = not bool(conn.closed) # "conn.closed" return 0 it's okey.
    
    return success, data
    
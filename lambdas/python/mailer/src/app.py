import json
import boto3
from botocore.exceptions import ClientError
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

ses_client = boto3.client('ses',region_name=os.environ.get('REGION'))
s3_client = boto3.client("s3")

# Try to send the email.
def lambda_handler(event, context):
    recipient = event["recipient"]
    file_name = event["file_name"]
    
    getPDF(file_name)
    send_email_with_attachment(recipient, file_name)

    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def getPDF(file_name):
    s3_client.download_file(os.environ.get("BUCKET"), 
                            "output/"+file_name,
                            "/tmp/"+file_name)
    return


def send_email_with_attachment(recipient, file_name):
    msg = MIMEMultipart()
    msg["Subject"] = os.environ.get('SUBJECT')
    msg["From"] = os.environ.get('SENDER')
    msg["To"] = recipient

    # Set message body
    body = MIMEText("Mail generado automaticamente. Por favor, no responder")
    msg.attach(body)

    part = MIMEApplication(open("/tmp/"+file_name, 'rb').read())

    part.add_header("Content-Disposition",
                        "attachment",
                        filename=file_name)
    msg.attach(part)

    # Convert message to string and send
    response = ses_client.send_raw_email(
        Source=os.environ.get('SENDER'),
        Destinations=[recipient],
        RawMessage={"Data": msg.as_string()}
    )
    print("Respuesta:")
    print(response)
    
    return

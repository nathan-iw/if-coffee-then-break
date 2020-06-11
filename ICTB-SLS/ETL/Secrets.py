import boto3
import json
import base64
from log import logger
from botocore.exceptions import ClientError

def get_secret():

    secret_name = "pocdbpw"
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
    )

    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
    else:
        secret = base64.b64decode(get_secret_value_response['SecretBinary'])

    secret = json.loads(secret)

    username = secret["username"]
    password = secret["password"]
    host = secret["host"]
    creds = [host, username, password, "poc_data"]

    logger.info("logger import worked!")
    return(creds)

get_secret()  
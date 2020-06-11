import json
from ETL.ETL import run_etl

def auto_etl(event, context):yaml.schemas
    body = {
        "message": "it fookin works mon!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    filename = event['Records'][0]['s3']['object']['key']
    run_etl(filename)
    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """

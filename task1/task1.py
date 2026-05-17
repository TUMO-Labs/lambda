import json

def lambda_handler(event, context):

    response = {
        "message": "Hello from Lambda",
        "method": event["requestContext"]["http"]["method"]
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }   

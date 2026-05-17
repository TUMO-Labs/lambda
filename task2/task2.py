import json

def lambda_handler(event, context):

    params = event.get("queryStringParameters")
    name = params.get("name") if params else "Guest"
    response = {
        "message": f"Hello {name}"
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }

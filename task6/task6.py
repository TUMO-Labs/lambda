import json

def lambda_handler(event, context):

    body = event.get("body")

    if body is None:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Missing body"})
        }
    try:
        data = json.loads(body)
    except:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid JSON"})
        }

    name = data.get("name")
    message = data.get("message")
    if not name or not message:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "name and message required"})
        }

    response = {
        "received": True,
        "name": name,
        "message": message
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }

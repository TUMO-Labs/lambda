import json

def lambda_handler(event, context):

    params = event.get("pathParameters") or {}

    username = params.get("username", "unknown")

    response = {
        "username": username,
        "profile": f"This is {username}'s profile"
    }

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(response)
    }
